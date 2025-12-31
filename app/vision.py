import random
from app.utils.logger import logger

def analyze_image(image_bytes: bytes):
    condition = "powdery_mildew"
    confidence = round(random.uniform(0.2, 0.6), 2)

    logger.info({
        "event": "vision_similarity",
        "condition": condition,
        "confidence": confidence
    })

    return [{
        "condition": condition,
        "confidence": confidence
    }]
