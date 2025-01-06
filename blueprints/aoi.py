from fastapi import APIRouter, HTTPException
from sqlalchemy import select, any_
from sqlalchemy.sql.expression import func
from typing import List
from database import database
from models.db_models import aois
from models.api_models import AOICreate, AOIResponse
import logging

aoi_router = APIRouter()

@aoi_router.post("/", response_model=AOIResponse)
async def create_aoi(aoi_data: AOICreate):
    query = aois.insert().values(**aoi_data.dict())
    last_record_id = await database.execute(query)
    return AOIResponse(id=last_record_id, **aoi_data.dict())

@aoi_router.get("/", response_model=List[AOIResponse])
async def get_aois():
    query = select(
        aois.c.id,
        aois.c.name,
        aois.c.customer_id,
        aois.c.country,
        aois.c.service_ids,
        aois.c.geom.ST_AsText().label("geom")  # Convert to WKT
    )
    result = await database.fetch_all(query)
    
    # Convert each record to a dictionary
    response = [
        {
            "id": row.id,
            "name": row.name,
            "customer_id": row.customer_id,
            "country": row.country,
            "service_ids": row.service_ids,
            "geom": row.geom
        }
        for row in result
    ]
    return response

@aoi_router.get("/match")
async def get_matching_aoi(customer_id: str, service_id: int, country: str):
    print("Received", customer_id,service_id, country )
    """
    Find an AOI that matches the customer_id, service_id, and country.
    """
    try:
        print("Trying")
        query = select(
            aois.c.id,
            aois.c.name,
            #aois.c.description,
            aois.c.customer_id,
            aois.c.country,
            aois.c.service_ids,
            aois.c.geom,
            func.ST_AsGeoJSON(aois.c.geom).label("geom")
        ).where(
            aois.c.customer_id == customer_id,
            country == aois.c.country,
            service_id == any_(aois.c.service_ids)
        )
        
        result = await database.fetch_one(query)

        if not result:
            raise HTTPException(status_code=404, detail="No matching AOI found")

        # Convert SQLAlchemy Row to dict and return
        return dict(result)

    except Exception as e:
        print("Error")
        raise HTTPException(status_code=500, detail=str(e))