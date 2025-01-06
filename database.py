from sqlalchemy import create_engine, MetaData, text
from databases import Database
from models.db_models import metadata
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#DATABASE_URL = "postgresql://postgres:postgres@10.0.0.200:5433/postgres"
DATABASE_URL = "postgresql://postgres:postgres@88.90.88.32:5433/postgres"

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# Create tables on startup
metadata.create_all(engine)

# Debug function to check data
async def check_data():
    try:
        query = text("SELECT * FROM ndvi_statistics")
        results = await database.fetch_all(query)
        logger.debug(f"Query results: {results}")
        return results
    except Exception as e:
        logger.error(f"Database error: {e}")
        return None