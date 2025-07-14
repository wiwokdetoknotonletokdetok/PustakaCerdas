import re
from uuid import UUID

from pydantic import BaseModel


def to_snake_case(string: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


class AmqpBookMessage(BaseModel):
    id: UUID
    title: str
    synopsis: str
    book_picture: str
    created_by: UUID

    class Config:
        alias_generator = to_snake_case
        validate_by_name = True
