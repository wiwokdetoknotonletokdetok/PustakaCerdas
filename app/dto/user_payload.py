from pydantic import BaseModel


class UserPayload(BaseModel):
    bookCount: int
