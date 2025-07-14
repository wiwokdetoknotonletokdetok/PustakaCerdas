import asyncio

from app.consumer.book_consumer import book_added_consumer
from app.consumer.book_consumer import book_updated_consumer
from fastapi import FastAPI


def setup_consumer(app: FastAPI):
    @app.on_event("startup")
    async def start_book_listener():
        asyncio.create_task(book_added_consumer())
        asyncio.create_task(book_updated_consumer())
