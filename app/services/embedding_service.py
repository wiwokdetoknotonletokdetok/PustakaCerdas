from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    _instance = None
    _model_name = "intfloat/multilingual-e5-small"

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = SentenceTransformer(cls._model_name)
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
