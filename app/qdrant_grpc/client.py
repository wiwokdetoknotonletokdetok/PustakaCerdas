import grpc
from flask import current_app

from generated import qdrant_pb2_grpc


class QdrantGrpcClient:
    def __init__(self):
        self.api_key = current_app.config["QDRANT_API_KEY"]
        self.host = current_app.config["QDRANT_GRPC_HOST"]
        self.port = current_app.config["QDRANT_GRPC_PORT"]
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = qdrant_pb2_grpc.QdrantStub(self.channel)
