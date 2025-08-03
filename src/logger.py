from loguru import logger
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "file.log")

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    LOG_FILE,
    rotation="1 day",  # Rotate every day
    level="INFO",      # Minimum level to log
    enqueue=True       # Use a queue for logging to avoid blocking
)
