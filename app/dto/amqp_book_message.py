from pydantic import BaseModel


class AmqpBookMessage(BaseModel):
    id: str
    title: str
    synopsis: str
    bookPicture: str
    createdBy: str
