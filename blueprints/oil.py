from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.sql import func
from geoalchemy2 import functions as geo_func
from typing import List
from database import database
from models.db_models import oil_slicks
from models.api_models import OilSlickCreate, OilSlickResponse

oil_router = APIRouter()

@oil_router.get("/", response_model=List[OilSlickResponse])
async def get_oil_slicks():
    # Use ST_AsText to convert geom to WKT
    query = select(
        oil_slicks.c.id,
        oil_slicks.c.type,
        oil_slicks.c.source_vessel,
        oil_slicks.c.certainty_percentage,
        func.ST_AsGeoJSON(oil_slicks.c.geom).label("geom")  # Convert geom to GeoJSON
    )
    results = await database.fetch_all(query)
    return [OilSlickResponse(**dict(r)) for r in results]

@oil_router.get("/{oil_slick_id}", response_model=OilSlickResponse)
async def get_oil_slick(oil_slick_id: int):
    query = oil_slicks.select().where(oil_slicks.c.id == oil_slick_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Oil slick not found")
    return OilSlickResponse(**dict(result))

@oil_router.post("/", response_model=OilSlickResponse)
async def create_oil_slick(oil_slick: OilSlickCreate):
    query = oil_slicks.insert().values(**oil_slick.dict())
    last_record_id = await database.execute(query)
    return OilSlickResponse(id=last_record_id, **oil_slick.dict())

@oil_router.delete("/{oil_slick_id}")
async def delete_oil_slick(oil_slick_id: int):
    query = oil_slicks.select().where(oil_slicks.c.id == oil_slick_id)
    existing_slick = await database.fetch_one(query)
    if not existing_slick:
        raise HTTPException(status_code=404, detail="Oil slick not found")
    delete_query = oil_slicks.delete().where(oil_slicks.c.id == oil_slick_id)
    await database.execute(delete_query)
    return {"message": f"Oil slick with ID {oil_slick_id} deleted successfully"}
