import asyncio

from app.consumer.book_consumer import book_consumer
from fastapi import FastAPI


def setup_consumer(app: FastAPI):
    @app.on_event("startup")
    async def start_book_listener():
        asyncio.create_task(book_consumer())
