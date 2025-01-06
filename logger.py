import logging

# Configure the global logger
logging.basicConfig(
    level=logging.DEBUG,  # Adjust log level as needed
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Ensure logs are output to the terminal
)

# Create and expose a single logger instance
logger = logging.getLogger("ndvi_algae_app")
