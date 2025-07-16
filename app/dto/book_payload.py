from pydantic import BaseModel


class BookPayload(BaseModel):
    id: str
    title: str
    bookPicture: str
