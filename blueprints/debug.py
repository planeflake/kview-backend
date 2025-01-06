from fastapi import APIRouter, HTTPException
import sys
import logging

# Explicitly set up logging to print to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Ensures logs print to console
        logging.FileHandler('debug.log')   # Log to file as well
    ]
)
logger = logging.getLogger(__name__)

# Print to stdout as well
print("DEBUGGING: Logger module loaded")

# Create a simple router for testing
debug_router = APIRouter(prefix="/debug")

@debug_router.get("/test")
async def debug_test():
    # Multiple logging methods to ensure something prints
    print("STDOUT: Debug test route hit")
    logger.info("LOGGER INFO: Debug test route accessed")
    logger.debug("LOGGER DEBUG: Detailed debug information")
    
    try:
        # Force a print to console
        sys.stdout.write("DIRECT STDOUT: Force console output\n")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error in debug route: {e}")
    
    return {"message": "Debug test successful"}