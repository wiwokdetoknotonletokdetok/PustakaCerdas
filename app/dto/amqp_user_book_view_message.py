from pydantic import BaseModel


class AmqpUserBookViewMessage(BaseModel):
    userId: str
    bookId: str
