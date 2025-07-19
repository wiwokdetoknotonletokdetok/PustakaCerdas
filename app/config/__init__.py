from fastapi import FastAPI
from qdrant_client.models import VectorParams, Distance

from app.config.qdrant_client import qdrant
from app.config.web_config import settings


def setup_database(app: FastAPI):
    @app.on_event("startup")
    def startup_event():
        if not qdrant.collection_exists(settings.book_collection):
            qdrant.create_collection(
                collection_name=settings.book_collection,
                vectors_config=VectorParams(size=settings.embedding_dimension, distance=Distance.COSINE)
            )

        if not qdrant.collection_exists(settings.user_collection):
            qdrant.create_collection(
                collection_name=settings.user_collection,
                vectors_config=VectorParams(size=settings.embedding_dimension, distance=Distance.COSINE)
            )
