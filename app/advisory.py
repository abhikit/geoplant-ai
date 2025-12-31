import time
from openai import OpenAI
from app.utils.logger import logger

client = OpenAI()

def generate_advice(question, env, vision, knowledge, history):
    start = time.time()

    prompt = f"""
Environment: {env}
Vision: {vision}
Knowledge: {knowledge}
Conversation history: {history}
User question: {question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    latency = int((time.time() - start) * 1000)

    logger.info({
        "event": "llm_call",
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
        "latency_ms": latency
    })

    return response.output_text
