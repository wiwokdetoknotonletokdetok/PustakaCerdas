from sentence_transformers import SentenceTransformer
from app.config import settings


class EmbeddingModel:
    _instance = None

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(settings.model_name, device=settings.model_device)
        return cls._instance


def get_query_embedding(text: str) -> list:
    return _get_embedding(text, "query")


def get_passage_embedding(text: str) -> list:
    return _get_embedding(text, "passage")


def _get_embedding(text: str, mode: str) -> list:
    model = EmbeddingModel.get_model()
    formatted = f"{mode}: {text.strip()}"
    embedding = model.encode(formatted, normalize_embeddings=True)
    return embedding.tolist()
