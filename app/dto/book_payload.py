from pydantic import BaseModel


class BookPayload(BaseModel):
    title: str
    synopsis: str
    book_picture: str
