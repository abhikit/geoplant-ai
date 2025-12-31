import logging
import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "geoplant.json.log"

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": "GeoPlantAI"
        }

        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        else:
            log_record["message"] = record.msg

        return json.dumps(log_record)

logger = logging.getLogger("GeoPlantAI")
logger.setLevel(logging.INFO)
logger.handlers = []

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(JsonFormatter())

console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())

logger.addHandler(file_handler)
logger.addHandler(console_handler)
