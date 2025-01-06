from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from services.ndvi_service import calculate_ndvi
from database import database
from models.db_models import algae_statistics, aois
from models.api_models import AOIResponse, AlgaeStatsCreate, AlgaeStatsResponse  # Import Pydantic models
from logger import logger

algae_router = APIRouter()

@algae_router.get("/", response_model=List[AlgaeStatsResponse])
async def get_algae():
    """
    Fetch all algae statistics.
    """
    try:
        query = algae_statistics.select()
        results = await database.fetch_all(query)
        logger.debug(f"Raw results: {results}")
        response_data = [AlgaeStatsResponse(**dict(r)) for r in results]
        logger.debug(f"Processed response data: {response_data}")
        return response_data
    except Exception as e:
        logger.error(f"Error in get_algae: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@algae_router.post("/", response_model=AlgaeStatsResponse)
async def create_algae(stats: AlgaeStatsCreate):
    """
    Create a new algae statistics entry.
    """
    query = algae_statistics.insert().values(
        **stats.dict(),
        created_at=datetime.now()
    )
    last_record_id = await database.execute(query)
    return AlgaeStatsResponse(
        id=last_record_id,
        **stats.dict(),
        created_at=datetime.now()
    )

@algae_router.get("/aoi", response_model=List[AOIResponse])
async def get_aoi(aoi_id: Optional[int] = None):
    """
    Fetch AOI details. If `aoi_id` is provided, fetch a single AOI.
    """
    if aoi_id:
        query = aois.select().where(aois.c.id == aoi_id)
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(status_code=404, detail="AOI not found")
        return AOIResponse(**dict(result))
    else:
        query = aois.select()
        results = await database.fetch_all(query)
        return [AOIResponse(**dict(result)) for result in results]

@algae_router.post("/aoi", response_model=AOIResponse)
async def create_aoi(name: str, geometry: str):
    """
    Create a new AOI entry.
    """
    query = aois.insert().values(
        name=name,
        geom=geometry
    )
    last_record_id = await database.execute(query)
    return AOIResponse(id=last_record_id, name=name, geom=geometry)

@algae_router.get("/stats", response_model=List[AlgaeStatsResponse])
async def get_algae_stats(
    aoi_id: Optional[int] = None,
    date: Optional[str] = None
):
    """
    Fetch algae statistics. Filter by AOI ID or date if provided.
    """
    query = algae_statistics.select()
    if aoi_id:
        query = query.where(algae_statistics.c.aoi == aoi_id)
    if date:
        query = query.where(algae_statistics.c.datetime == date)
    results = await database.fetch_all(query)
    return [AlgaeStatsResponse(**dict(r)) for r in results]

@algae_router.post("/stats", response_model=AlgaeStatsResponse)
async def create_algae_stats(stats: AlgaeStatsCreate):
    """
    Create a new algae statistics entry.
    """
    query = algae_statistics.insert().values(
        **stats.dict(),
        created_at=datetime.now()
    )
    last_record_id = await database.execute(query)
    return AlgaeStatsResponse(
        id=last_record_id,
        **stats.dict(),
        created_at=datetime.now()
    )
