from fastapi import FastAPI

from app.config import setup_database
from app.consumer import setup_consumer
from app.controller import book_router
from app.controller import recommendation_router

app = FastAPI()

app.include_router(book_router)
app.include_router(recommendation_router)

setup_consumer(app)

setup_database(app)
