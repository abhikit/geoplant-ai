import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from app.utils.logger import logger

# --------------------------------------------------
# Load environment variables safely
# --------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Please set it in .env file."
    )

client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------
# Advisory Generator
# --------------------------------------------------
def generate_advice(
    question: str,
    environment: dict,
    vision_analysis: list,
    knowledge: list,
    conversation_history: list
):
    start_time = time.time()

    # --------------------------------------------------
    # Prepare vision summary safely (ALWAYS defined)
    # --------------------------------------------------
    if vision_analysis and isinstance(vision_analysis, list):
        vision_summary_text = ", ".join(
            f"{v.get('condition', 'unknown')} ({round(v.get('confidence', 0) * 100, 1)}%)"
            for v in vision_analysis
        )
    else:
        vision_summary_text = (
            "No plant image was provided. "
            "Advice is based only on local environmental conditions and user query."
        )

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------
    prompt = f"""
You are GeoPlant AI, a location-aware plant health advisory system.

IMPORTANT:
The advice you generate MUST be grounded in the LOCAL ENVIRONMENTAL CONDITIONS
of the selected location and the plant’s visual condition (if image is provided).

LOCATION CONTEXT:
- City / Area: {environment.get("city", "User-selected location")}
- Latitude: {environment.get("lat", "N/A")}
- Longitude: {environment.get("lon", "N/A")}

LOCAL ENVIRONMENTAL FACTORS:
- Temperature: {environment.get("temperature", "Not available")} °C
- Humidity: {environment.get("humidity", "Not available")} %
- Air Quality Index (AQI): {environment.get("aqi", "Not available")}
- Soil Type: {environment.get("soil_type", "Unknown / Not available")}
- Water Stress Indicator: {environment.get("water_stress", "Not available")}

PLANT VISUAL ANALYSIS:
{vision_summary_text}

USER QUESTION:
{question if question else "No explicit question asked. Provide a general plant health advisory based on location and plant condition."}

INSTRUCTIONS:
- Clearly explain HOW the local environmental conditions may be impacting the plant.
- Avoid generic plant advice.
- Explicitly mention the role of AQI, humidity, temperature, soil, or water stress where relevant.
- If unsure, state uncertainty clearly.

Provide a structured response with:
1. Observations
2. Environmental Impact Explanation
3. Practical Care Recommendations
4. Disclaimer
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    latency_ms = int((time.time() - start_time) * 1000)

    logger.info({
        "event": "llm_call",
        "model": "gpt-4.1-mini",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.total_tokens,
        "latency_ms": latency_ms
    })

    return response.output_text
