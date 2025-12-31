from PIL import Image
from sentence_transformers import SentenceTransformer
import io

model = SentenceTransformer("clip-ViT-B-32")

def embed_uploaded_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return model.encode(image).tolist()
