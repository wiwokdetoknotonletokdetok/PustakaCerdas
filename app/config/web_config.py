from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_api_key: str
    qdrant_grpc_host: str
    qdrant_grpc_port: int
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_pass: str

    class Config:
        env_file = ".env"


settings = Settings()