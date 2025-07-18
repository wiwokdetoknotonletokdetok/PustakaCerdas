import numpy as np

from app.config import qdrant, settings
from app.dto import BookPayload


def get_book_recommendations(user_id: str, top_k: int):
    vector = normalize_vector(np.random.rand(384).tolist())

    search_result = qdrant.search(
        collection_name=settings.collection_name,
        query_vector=vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    books: list[BookPayload] = []

    for point in search_result:
        payload = point.payload
        try:
            book = BookPayload(**payload)
            books.append(book)
        except Exception as e:
            print(f"Payload error: {e}, data: {payload}")

    return books


def normalize_vector(vec: list[float]) -> list[float]:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return (np.array(vec) / norm).tolist()
