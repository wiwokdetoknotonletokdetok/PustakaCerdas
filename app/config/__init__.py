from fastapi import FastAPI
from qdrant_client.models import VectorParams, Distance

from app.config.qdrant_client import qdrant
from app.config.web_config import settings


def setup_database(app: FastAPI):
    @app.on_event("startup")
    def startup_event():
        if not qdrant.collection_exists(settings.collection_name):
            qdrant.create_collection(
                collection_name=settings.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
