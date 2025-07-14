from qdrant_client.models import PointStruct

from app.config import qdrant, settings
from app.dto import AmqpBookMessage, BookPayload
from app.services.embedding_service import get_passage_embedding, get_query_embedding


def save_book(message: AmqpBookMessage):
    passage = get_passage_embedding(f"{message.title}. {message.synopsis}")

    book_payload = BookPayload(**message.dict())

    qdrant.upsert(
        collection_name=settings.collection_name,
        points=[PointStruct(id=str(message.id), vector=passage, payload=book_payload.dict())]
    )


def search_book(query: str, top_k: int = 5) -> list[BookPayload]:
    query_vector = get_query_embedding(query)

    search_result = qdrant.search(
        collection_name=settings.collection_name,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
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
