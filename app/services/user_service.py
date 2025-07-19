import asyncio

import numpy as np
from qdrant_client.models import PointStruct

from app.config import qdrant, settings
from app.dto import AmqpUserRegisteredMessage, AmqpUserBookViewMessage
from app.dto.user_payload import UserPayload


def init_user_embedding(user_id: str):
    initial_vector = np.zeros(settings.embedding_dimension, dtype=np.float32).tolist()

    user_payload = UserPayload(short_term_ids=[])

    qdrant.upsert(
        collection_name=settings.user_collection,
        points=[
            PointStruct(
                id=user_id,
                vector=initial_vector,
                payload=user_payload.dict()
            )
        ]
    )


async def save_user(message: AmqpUserRegisteredMessage):
    await asyncio.to_thread(init_user_embedding, message.userId)


async def update_user_embedding(message: AmqpUserBookViewMessage):
    SHORT_TERM_LIMIT = 8
    DECAY_ALPHA = 0.1

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
        user_payload = UserPayload(short_term_ids=[message.bookId])
        long_term_vector = book_vector
    else:
        user_point = user_result[0]
        old_vector = np.array(user_point.vector)
        user_payload = UserPayload(**user_point.payload)

        long_term_vector = (1 - DECAY_ALPHA) * old_vector + DECAY_ALPHA * book_vector

        stm_ids = user_payload.short_term_ids or []
        stm_ids.append(message.bookId)
        if len(stm_ids) > SHORT_TERM_LIMIT:
            stm_ids = stm_ids[-SHORT_TERM_LIMIT:]
        user_payload.short_term_ids = stm_ids

    short_term_vectors = []
    if user_payload.short_term_ids:
        short_term_result = qdrant.retrieve(
            collection_name=settings.book_collection,
            ids=user_payload.short_term_ids,
            with_payload=False,
            with_vectors=True
        )
        short_term_vectors = [np.array(b.vector) for b in short_term_result if b.vector]

    if short_term_vectors:
        short_term_avg = np.mean(short_term_vectors, axis=0)
        final_vector = 0.7 * long_term_vector + 0.3 * short_term_avg
    else:
        final_vector = long_term_vector

    norm = np.linalg.norm(final_vector)
    if norm != 0:
        final_vector = final_vector / norm

    await asyncio.to_thread(
        qdrant.upsert,
        collection_name=settings.user_collection,
        points=[
            PointStruct(
                id=message.userId,
                vector=final_vector.astype(np.float32).tolist(),
                payload=user_payload.dict()
            )
        ]
    )
