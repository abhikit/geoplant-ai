import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

KNOWLEDGE_DIR = "knowledge"
OUTPUT_FILE = "embeddings.json"

# ---------------------------------------
# Helper: simple semantic chunking
# ---------------------------------------
def chunk_text(text):
    """
    Splits text by blank lines.
    Each paragraph = one semantic chunk.
    """
    chunks = []
    for chunk in text.split("\n\n"):
        clean = chunk.strip()
        if len(clean) > 50:
            chunks.append(clean)
    return chunks

# ---------------------------------------
# Main embedding pipeline
# ---------------------------------------
all_chunks = []

for filename in os.listdir(KNOWLEDGE_DIR):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(KNOWLEDGE_DIR, filename)

    with open(filepath, "r") as f:
        text = f.read()

    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding

        all_chunks.append({
            "text": chunk,
            "embedding": embedding,
            "source": filename
        })

# ---------------------------------------
# Save embeddings locally
# ---------------------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(all_chunks, f)

print(f"Saved {len(all_chunks)} embeddings to {OUTPUT_FILE}")
