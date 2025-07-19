from pydantic import BaseModel


class AmqpUserRegisteredMessage(BaseModel):
    userId: str
