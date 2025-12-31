import json
import numpy as np
import faiss
from pathlib import Path
from collections import defaultdict

# 🚫 NO imports from app.vision.image_search here

BASE_DIR = Path(__file__).resolve().parents[2]
EMB_FILE = BASE_DIR / "data" / "image_embeddings.json"


class ImageSimilarityEngine:
    def __init__(self):
        with open(EMB_FILE, "r") as f:
            data = json.load(f)

        self.labels = [d["condition"] for d in data]
        self.embeddings = np.array(
            [d["embedding"] for d in data],
            dtype=np.float32
        )

        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, embedding, top_k=5):
        vector = np.array([embedding], dtype=np.float32)
        distances, indices = self.index.search(vector, top_k)

        scores = defaultdict(list)
        for idx, dist in zip(indices[0], distances[0]):
            confidence = float(np.exp(-float(dist)))
            scores[self.labels[int(idx)]].append(confidence)

        results = []
        for condition, vals in scores.items():
            results.append({
                "condition": condition.replace("_", " ").title(),
                "confidence": round(sum(vals) / len(vals), 3)
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
