import json
from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "plant_diseases"
OUT_FILE = BASE_DIR / "data" / "image_embeddings.json"

model = SentenceTransformer("clip-ViT-B-32")

records = []

for disease_dir in DATA_DIR.iterdir():
    if not disease_dir.is_dir():
        continue

    condition = disease_dir.name

    for img_path in disease_dir.iterdir():
        if img_path.suffix.lower() not in [".jpg", ".png", ".jpeg"]:
            continue

        image = Image.open(img_path).convert("RGB")
        embedding = model.encode(image).tolist()

        records.append({
            "condition": condition,
            "image": img_path.name,
            "embedding": embedding
        })

        print(f"Embedded: {condition}/{img_path.name}")

with open(OUT_FILE, "w") as f:
    json.dump(records, f)

print(f"\n✅ Saved {len(records)} embeddings to {OUT_FILE}")
