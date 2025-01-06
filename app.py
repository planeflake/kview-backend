from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import logging

# Explicit logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Ensures logs print to console
        logging.FileHandler('app_full_debug.log')  # Comprehensive log file
    ]
)
logger = logging.getLogger(__name__)

# Print to stdout to verify logging
print("DEBUGGING: App module loaded")

from database import database
from blueprints.ndvi import ndvi_router
from blueprints.algae import algae_router
from blueprints.debug import debug_router  # Import the new debug router
from blueprints.vessel import vessel_router
from blueprints.oil import oil_router
from blueprints.aoi import aoi_router
from blueprints.customer import customer_router
from blueprints.service import service_router
from blueprints.locations import location_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info("Starting application...")
    try:
        await database.connect()
        logger.debug("Database connected successfully")

        # Print registered routes for debugging
        logger.info("Available routes:")
        for route in app.routes:
            logger.info(f"Route: {route.path} Methods: {route.methods}")
        yield
    finally:
        # Shutdown code
        logger.info("Shutting down application...")
        await database.disconnect()
        logger.debug("Database disconnected successfully")
app = FastAPI(
    title="Emerging Products and Services Portal API",
    description="API for delivery of data to the EPS portal",
    version="0.1",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response


# Include routers

app.include_router(algae_router, prefix="/service/algae", tags=["Algae"])
app.include_router(ndvi_router, prefix="/service/ndvi", tags=["NDVI"])
app.include_router(vessel_router, prefix="/service/vessels", tags=["Vessels"])
app.include_router(oil_router, prefix="/service/oil", tags=["Oil"])
app.include_router(debug_router, prefix="/debug", tags=["Debug"])
app.include_router(customer_router, prefix="/customer", tags=["Customer"])
app.include_router(aoi_router, prefix="/aoi", tags=["Aois"])
app.include_router(service_router, prefix="", tags=["Service"])
app.include_router(location_router, prefix="/locations", tags=["Locations"])