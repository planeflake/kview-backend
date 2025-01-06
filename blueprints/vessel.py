from fastapi import APIRouter, HTTPException
from typing import List
from shapely.wkb import loads
from database import database
from models.db_models import vessel
from models.api_models import VesselCreate, VesselUpdate, VesselResponse
from sqlalchemy import Column, Integer
from shapely.geometry import mapping
import logging

logger = logging.getLogger(__name__)
vessel_router = APIRouter()

@vessel_router.get("/", response_model=List[VesselResponse])
async def get_all_vessels():
    """
    Fetch all vessels.
    """
    query = vessel.select()
    results = await database.fetch_all(query)
    response_data = []
    for r in results:
        data = dict(r)
        data["geom"] = mapping(loads(data["geom"]))  # Convert WKB to GeoJSON
        response_data.append(VesselResponse(**data))
    return response_data

@vessel_router.get("/by-id/{vessel_id}", response_model=VesselResponse)
async def get_vessel_by_id(vessel_id: int):
    """
    Fetch a single vessel by ID.
    """
    query = vessel.select().where(vessel.c.id == vessel_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Vessel not found")
    data = dict(result)
    data["geom"] = mapping(loads(data["geom"]))  # Convert WKB to GeoJSON
    return VesselResponse(**data)

@vessel_router.get("/by-location/{location_id}", response_model=List[VesselResponse])
async def get_vessels_by_location(location_id: int):
    """
    Fetch all vessels by location.
    """
    query = vessel.select().where(vessel.c.location_id == location_id)
    results = await database.fetch_all(query)

    if not results:
        raise HTTPException(status_code=404, detail="No vessels found for this location.")

    vessels = []
    for result in results:
        data = dict(result)
        data["geom"] = mapping(loads(data["geom"]))  # Convert WKB to GeoJSON
        vessels.append(VesselResponse(**data))

    return vessels

@vessel_router.post("/", response_model=VesselResponse)
async def create_vessel(vessel_data: VesselCreate):
    """
    Create a new vessel entry.
    """
    query = vessel.insert().values(**vessel_data.dict())
    last_record_id = await database.execute(query)
    return VesselResponse(id=last_record_id, **vessel_data.dict())

@vessel_router.put("/{vessel_id}", response_model=VesselResponse)
async def update_vessel(vessel_id: int, vessel_data: VesselUpdate):
    """
    Update an existing vessel.
    """
    query = vessel.select().where(vessel.c.id == vessel_id)
    existing_vessel = await database.fetch_one(query)
    if not existing_vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    update_data = {key: value for key, value in vessel_data.dict().items() if value is not None}
    update_query = vessel.update().where(vessel.c.id == vessel_id).values(**update_data)
    await database.execute(update_query)

    updated_vessel = await database.fetch_one(vessel.select().where(vessel.c.id == vessel_id))
    data = dict(updated_vessel)
    data["geom"] = loads(data["geom"]).wkt  # Convert WKB to WKT
    return VesselResponse(**data)

@vessel_router.delete("/{vessel_id}")
async def delete_vessel(vessel_id: int):
    """
    Delete a vessel by ID.
    """
    query = vessel.select().where(vessel.c.id == vessel_id)
    existing_vessel = await database.fetch_one(query)
    if not existing_vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    delete_query = vessel.delete().where(vessel.c.id == vessel_id)
    await database.execute(delete_query)
    return {"message": f"Vessel with ID {vessel_id} deleted successfully"}

