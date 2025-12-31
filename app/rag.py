from app.utils.logger import logger

KNOWLEDGE_BASE = [
    "Yellow leaves can indicate nitrogen deficiency.",
    "Overwatering may cause root stress.",
    "High pollution can reduce photosynthesis efficiency."
]

def retrieve_knowledge(query: str):
    chunks = KNOWLEDGE_BASE[:2]

    logger.info({
        "event": "rag_retrieval",
        "chunks_used": chunks
    })

    return chunks
