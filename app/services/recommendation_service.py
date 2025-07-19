import numpy as np

from app.config import qdrant, settings
from app.dto import BookPayload


def get_book_recommendations(user_id: str, top_k: int):
    if user_id:
        user_result = qdrant.retrieve(
            collection_name=settings.user_collection,
            ids=[user_id],
            with_payload=False,
            with_vectors=True
        )

        user_point = user_result[0]
        vector = user_point.vector
    else:
        vector = normalize_vector(np.random.rand(settings.embedding_dimension).tolist())

    search_result = qdrant.search(
        collection_name=settings.book_collection,
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
