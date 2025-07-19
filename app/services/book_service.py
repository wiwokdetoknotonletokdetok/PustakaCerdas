import asyncio

from qdrant_client.models import PointStruct

from app.config import qdrant, settings
from app.dto import AmqpBookMessage, BookPayload
from app.services.embedding_service import get_embedding


async def save_book(message: AmqpBookMessage):
    passage = await asyncio.to_thread(get_embedding, f"{message.title}. {message.synopsis}")

    book_payload = BookPayload(**message.dict())

    await asyncio.to_thread(
        qdrant.upsert,
        collection_name=settings.book_collection,
        points=[PointStruct(id=message.id, vector=passage, payload=book_payload.dict())]
    )


async def update_book_payload(message: AmqpBookMessage):
    new_payload = BookPayload(**message.dict())

    await asyncio.to_thread(
        qdrant.overwrite_payload,
        collection_name=settings.book_collection,
        points=[message.id],
        payload=new_payload.dict()
    )


def search_book(query: str, top_k: int, score_threshold: float) -> list[BookPayload]:
    query_vector = get_embedding(query)

    search_result = qdrant.search(
        collection_name=settings.book_collection,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        with_vectors=False
    )

    books: list[BookPayload] = []

    for point in search_result:
        if point.score is not None and point.score >= score_threshold:
            payload = point.payload
            try:
                book = BookPayload(**payload)
                books.append(book)
            except Exception as e:
                print(f"Payload error: {e}, data: {payload}")

    return books
