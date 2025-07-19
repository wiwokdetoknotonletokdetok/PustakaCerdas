import asyncio

import numpy as np
from qdrant_client.models import PointStruct

from app.config import qdrant, settings
from app.dto import AmqpUserRegisteredMessage, AmqpUserBookViewMessage
from app.dto.user_payload import UserPayload


async def save_user(message: AmqpUserRegisteredMessage):
    initial_vector = np.zeros(settings.embedding_dimension, dtype=np.float32).tolist()

    user_payload = UserPayload(bookCount=0)

    await asyncio.to_thread(
        qdrant.upsert,
        collection_name=settings.user_collection,
        points=[
            PointStruct(
                id=message.userId,
                vector=initial_vector,
                payload=user_payload.dict()
            )
        ]
    )


async def update_user_embedding(message: AmqpUserBookViewMessage):
    book_result = qdrant.retrieve(
        collection_name=settings.book_collection,
        ids=[message.bookId],
        with_payload=False,
        with_vectors=True
    )

    if not book_result or len(book_result) == 0:
        raise ValueError(f"Book with id {message.bookId} not found")

    book_vector = np.array(book_result[0].vector)

    user_result = qdrant.retrieve(
        collection_name=settings.user_collection,
        ids=[message.userId],
        with_payload=True,
        with_vectors=True
    )

    if not user_result or len(user_result) == 0:
        updated_vector = book_vector.astype(np.float32).tolist()
        user_payload = UserPayload(bookCount=1)
    else:
        user_point = user_result[0]
        old_vector = np.array(user_point.vector)
        user_payload = UserPayload(**user_point.payload)

        user_payload.bookCount += 1
        updated_vector = old_vector + (book_vector - old_vector) / user_payload.bookCount

        norm = np.linalg.norm(updated_vector)
        if norm != 0:
            updated_vector = updated_vector / norm

        updated_vector = updated_vector.astype(np.float32).tolist()

    await asyncio.to_thread(
        qdrant.upsert,
        collection_name=settings.user_collection,
        points=[
            PointStruct(
                id=message.userId,
                vector=updated_vector,
                payload=user_payload.dict()
            )
        ]
    )
