from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import json

from app.utils.logger import logger
from app.environment import get_environment
from app.vision import analyze_image
from app.rag import retrieve_knowledge
from app.advisory.plant_advisor import generate_advice

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI(title="GeoPlant AI 🌱")

# --------------------------------------------------
# Frontend
# --------------------------------------------------
@app.get("/")
def home():
    return FileResponse("static/index.html")

# --------------------------------------------------
# Conversational Chat Endpoint
# --------------------------------------------------
@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...),
    question: str = Form(""),
    conversation: str = Form(""),
    image: UploadFile | None = None
):
    # -----------------------------
    # Safe conversation parsing
    # -----------------------------
    try:
        history = json.loads(conversation)
        if not isinstance(history, list):
            history = []
    except Exception:
        history = []

    logger.info({
        "event": "request_received",
        "session_id": session_id,
        "lat": lat,
        "lon": lon,
        "question_present": bool(question),
        "image_present": image is not None,
        "history_length": len(history)
    })

    # -----------------------------
    # Environment data
    # -----------------------------
    environment = get_environment(lat, lon, WEATHER_API_KEY)

    # -----------------------------
    # Vision (optional)
    # -----------------------------
    vision_result = []
    if image:
        image_bytes = await image.read()
        vision_result = analyze_image(image_bytes)

    # -----------------------------
    # Knowledge (RAG)
    # -----------------------------
    knowledge = retrieve_knowledge(question)

    # -----------------------------
    # Generate advisory
    # -----------------------------
    answer = generate_advice(
        question=question,
        environment=environment,
        vision_analysis=vision_result,
        knowledge=knowledge,
        conversation_history=history
    )

    # -----------------------------
    # Update conversation memory
    # -----------------------------
    history.append({
        "user": question if question else "[No explicit question]",
        "assistant": answer
    })

    # Keep last 5 turns only (production best practice)
    history = history[-5:]

    logger.info({
        "event": "response_sent",
        "session_id": session_id,
        "history_length": len(history)
    })

    return {
        "environment": environment,
        "vision": vision_result,
        "answer": answer,
        "conversation": history
    }
