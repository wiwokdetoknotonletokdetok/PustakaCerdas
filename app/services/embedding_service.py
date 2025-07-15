from sentence_transformers import SentenceTransformer
from app.config import settings


class EmbeddingModel:
    _instance = None

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.model_name, device=settings.model_device)
        return cls._instance


def get_embedding(text: str) -> list:
    model = EmbeddingModel.get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
