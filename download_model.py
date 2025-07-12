from sentence_transformers import SentenceTransformer
from app.config import settings

model = SentenceTransformer(settings.model_name, device=settings.model_device)
