from app.dto import AmqpBookMessage
from app.services.embedding_service import get_passage_embedding


def save_new_book(message: AmqpBookMessage):
    passage = get_passage_embedding(f"{message.title}. {message.synopsis}")
