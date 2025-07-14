import asyncio

from fastapi import FastAPI

from app.listener.book_listener import book_added_listener
from app.listener.book_listener import book_updated_listener


def setup_listener(app: FastAPI):
    @app.on_event("startup")
    async def start_book_listener():
        asyncio.create_task(book_added_listener())
        asyncio.create_task(book_updated_listener())
