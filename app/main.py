from fastapi import FastAPI

from app.config import setup_database
from app.controller import book_router
from app.consumer import setup_consumer

app = FastAPI()

app.include_router(book_router)

setup_consumer(app)

setup_database(app)
