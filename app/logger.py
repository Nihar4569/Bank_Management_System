import logging
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logging (to file)
logging.basicConfig(
    filename="logs/bms_app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ✅ Define logger instance (this is what crud.py imports)
logger = logging.getLogger("bms_logger")
logger.setLevel(logging.INFO)
