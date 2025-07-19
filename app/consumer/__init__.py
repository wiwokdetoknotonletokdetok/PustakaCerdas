import asyncio

from app.consumer.book_consumer import book_consumer
from app.consumer.user_consumer import user_consumer
from fastapi import FastAPI


def setup_consumer(app: FastAPI):
    @app.on_event("startup")
    async def start_consumer():
        asyncio.create_task(book_consumer())
        asyncio.create_task(user_consumer())
