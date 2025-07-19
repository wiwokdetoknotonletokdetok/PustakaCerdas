import json

from aio_pika import connect_robust, IncomingMessage

from app.config import settings
from app.dto import AmqpBookMessage
from app.services import save_book, update_book_payload


async def handle_book_message(message: IncomingMessage):
    async with message.process():
        routing_key = message.routing_key
        raw_body = message.body.decode()

        data = json.loads(raw_body)
        book_message = AmqpBookMessage.parse_obj(data)

        if routing_key == "book.created":
            await save_book(book_message)
        elif routing_key == "book.picture.added":
            await update_book_payload(book_message)


async def book_consumer():
    QUEUE_BOOK = "pustakacerdas.book.queue"

    connection = await connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue(QUEUE_BOOK, durable=True)
    await queue.consume(handle_book_message)
