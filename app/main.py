from fastapi import FastAPI

from app.config import setup_database
from app.controller import book_router
from app.listener import setup_listener

app = FastAPI()

app.include_router(book_router)

setup_listener(app)

setup_database(app)
