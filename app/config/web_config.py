from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_api_key: str
    qdrant_grpc_host: str
    qdrant_grpc_port: int
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_pass: str
    model_name: str = "all-MiniLM-L6-v2"
    model_device: str = "cpu"
    book_collection: str = "book"
    user_collection: str = "user"
    embedding_dimension: int = 384
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    @property
    def rabbitmq_url(self):
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    class Config:
        env_file = ".env"


settings = Settings()
