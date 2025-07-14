import json

from aio_pika import connect_robust, IncomingMessage

from app.config import settings
from app.dto import AmqpBookMessage
from app.services import save_new_book


async def handle_book_message(message: IncomingMessage):
    async with message.process():
        raw_body = message.body.decode()
        data = json.loads(raw_body)

        book_message = AmqpBookMessage.parse_obj(data)
        save_new_book(book_message)


async def book_added_consumer():
    connection = await connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue("book.added", durable=True)
    await queue.consume(handle_book_message)


async def book_updated_consumer():
    connection = await connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue("book.updated", durable=True)
    await queue.consume(handle_book_message)
