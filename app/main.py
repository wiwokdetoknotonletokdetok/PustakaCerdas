from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import setup_database, settings
from app.consumer import setup_consumer
from app.controller import book_router
from app.controller import recommendation_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins.split(","),
    allow_methods=["GET"],
    allow_headers=settings.cors_allowed_headers.split(","),
)

app.include_router(book_router)
app.include_router(recommendation_router)

setup_consumer(app)

setup_database(app)
