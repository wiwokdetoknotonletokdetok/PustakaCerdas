import numpy as np
from qdrant_client.models import Filter, FieldCondition, MatchAny

from app.config import qdrant, settings
from app.dto import BookPayload


def get_book_recommendations(user_id: str, top_k: int):
    short_term_ids = []
    vector = None
    query_filter = None

    if user_id:
        user_result = qdrant.retrieve(
            collection_name=settings.user_collection,
            ids=[user_id],
            with_payload=True,
            with_vectors=True
        )

        if not user_result:
            raise ValueError(f"User {user_id} not found")

        user_point = user_result[0]
        vector = user_point.vector

        user_payload = user_point.payload
        short_term_ids = user_payload.get("short_term_ids")

        print(short_term_ids)

        if short_term_ids:
            query_filter = Filter(
                must_not=[
                    FieldCondition(
                        key="id",
                        match=MatchAny(any=short_term_ids)
                    )
                ]
            )

    if vector:
        limit = top_k + len(short_term_ids)
        search_result = qdrant.search(
            collection_name=settings.book_collection,
            query_vector=vector,
            limit=limit,
            with_payload=True,
            with_vectors=False,
            query_filter=query_filter
        )
    else:
        vector = normalize_vector(np.random.rand(settings.embedding_dimension).tolist())

        search_result = qdrant.search(
            collection_name=settings.book_collection,
            query_vector=vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
            query_filter=query_filter
        )

    books: list[BookPayload] = []

    for point in search_result:
        payload = point.payload
        try:
            book = BookPayload(**payload)
            books.append(book)
        except Exception as e:
            print(f"Payload error: {e}, data: {payload}")

    return books[:top_k]


def normalize_vector(vec: list[float]) -> list[float]:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return (np.array(vec) / norm).tolist()
