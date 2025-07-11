from qdrant_client import QdrantClient

from app.config.web_config import settings

qdrant = QdrantClient(
    host=settings.qdrant_grpc_host,
    port=settings.qdrant_grpc_port,
    prefer_grpc=True,
    https=False,
    api_key=settings.qdrant_api_key
)
