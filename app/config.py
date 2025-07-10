import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = "HS256"
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_GRPC_HOST = os.getenv("QDRANT_GRPC_HOST")
    QDRANT_GRPC_PORT = os.getenv("QDRANT_GRPC_PORT")
