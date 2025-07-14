from uuid import UUID

from pydantic import BaseModel


def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class AmqpBookMessage(BaseModel):
    id: UUID
    title: str
    synopsis: str
    book_picture: str
    created_by: UUID

    class Config:
        alias_generator = to_camel
        validate_by_name = True
