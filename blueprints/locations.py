from models.api_models import LocationCreate, LocationResponse, LocationBase
from fastapi import APIRouter, HTTPException
from models.db_models import locations
from database import database
from typing import List
from logger import logger
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import select
from models.api_models import LocationCreate, LocationResponse, LocationBase
from geoalchemy2.shape import WKBElement
from geoalchemy2.functions import ST_AsGeoJSON
from sqlalchemy import select
import json

location_router = APIRouter()


@location_router.get("/", response_model=List[LocationBase])
async def get_locations():
    try:
        query = """
            SELECT 
                id, 
                name, 
                description, 
                country, 
                iso3, 
                customer_id,
                ST_AsGeoJSON(coords)::json as coords,
                ST_AsGeoJSON(countrycoords)::json as countrycoords
            FROM locations
        """
        result = await database.fetch_all(query)
        
        locations_list = []
        for row in result:
            location_dict = dict(row)
            # Parse the JSON strings into dictionaries
            if location_dict['coords']:
                location_dict['coords'] = json.loads(location_dict['coords'])
            if location_dict['countrycoords']:
                location_dict['countrycoords'] = json.loads(location_dict['countrycoords'])
            
            locations_list.append(LocationBase.model_validate(location_dict))

        return locations_list

    except Exception as e:
        logger.error(f"Error fetching locations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@location_router.get("/customer/{customer_id}", response_model=List[LocationBase])
async def get_locations_by_customer(customer_id: str):
    try:
        query = """
            SELECT 
                id, 
                name, 
                description, 
                country, 
                iso3, 
                customer_id,
                ST_AsGeoJSON(coords)::json as coords,
                ST_AsGeoJSON(countrycoords)::json as countrycoords
            FROM locations
            WHERE customer_id = :customer_id
        """
        result = await database.fetch_all(query, values={"customer_id": customer_id})
        
        locations_list = []
        for row in result:
            location_dict = dict(row)
            # Parse the JSON strings into dictionaries
            if location_dict['coords']:
                location_dict['coords'] = json.loads(location_dict['coords'])
            if location_dict['countrycoords']:
                location_dict['countrycoords'] = json.loads(location_dict['countrycoords'])
            
            locations_list.append(LocationBase.model_validate(location_dict))

        return locations_list

    except Exception as e:
        logger.error(f"Error fetching locations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@location_router.post("/", response_model=LocationResponse)
async def create_location(location_data: LocationCreate):
    try:
        query = locations.__table__.insert().values(**location_data.model_dump())
        location_id = await database.execute(query)
        logger.debug(f"Inserted location with ID: {location_id}")
        return {"id": location_id, **location_data.model_dump()}
    except Exception as e:
        logger.error(f"Error inserting location: {e}")
        raise HTTPException(status_code=500, detail="Error creating location.")