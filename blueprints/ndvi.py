from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from services.ndvi_service import calculate_ndvi
from database import database
from models.db_models import ndvi_statistics, aois
from models.api_models import NDVIStatsCreate, NDVIResponse, AOIResponse  # Import Pydantic models
from logger import logger

ndvi_router = APIRouter()

@ndvi_router.get("/", response_model=List[NDVIResponse])

async def get_ndvi():
    try:
        query = ndvi_statistics.select()
        results = await database.fetch_all(query)
        logger.debug(f"Raw results: {results}")
        # Convert records to model instances
        response_data = [NDVIResponse(**dict(r)) for r in results]
        logger.debug(f"Processed response data: {response_data}")
        return response_data
    except Exception as e:
        logger.error(f"Error in get_ndvi: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@ndvi_router.post("/")
async def create_ndvi(filepath: str):
    result = calculate_ndvi(filepath)
    return {"message": "NDVI created successfully", "data": result}

@ndvi_router.get("/aoi", response_model=AOIResponse)
async def get_aoi(aoi_id: int):
    query = aois.select().where(aois.c.id == aoi_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="AOI not found")
    return AOIResponse(**dict(result))

@ndvi_router.post("/aoi")
async def create_aoi(name: str, geometry: str):
    query = aois.insert().values(
        name=name,
        geom=geometry
    )
    last_record_id = await database.execute(query)
    return {"message": "AOI created successfully", "id": last_record_id}

@ndvi_router.get("/stats", response_model=List[NDVIResponse])
async def get_ndvi_stats(
    aoi_id: Optional[int] = None,
    date: Optional[str] = None
):
    query = ndvi_statistics.select()
    if aoi_id:
        query = query.where(ndvi_statistics.c.aoi_id == aoi_id)
    if date:
        query = query.where(ndvi_statistics.c.date == date)
    results = await database.fetch_all(query)
    return [NDVIResponse(**dict(r)) for r in results]

@ndvi_router.post("/stats", response_model=NDVIResponse)
async def create_ndvi_stats(stats: NDVIStatsCreate):
    query = ndvi_statistics.insert().values(
        **stats.dict(),
        created_at=datetime.now()
    )
    last_record_id = await database.execute(query)
    return NDVIResponse(
        id=last_record_id,
        **stats.dict(),
        created_at=datetime.now()
    )
