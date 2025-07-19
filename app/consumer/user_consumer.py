import json

from aio_pika import connect_robust, IncomingMessage

from app.config import settings
from app.dto import AmqpUserRegisteredMessage, AmqpUserBookViewMessage
from app.services import save_user, update_user_embedding


async def handle_user_message(message: IncomingMessage):
    async with message.process():
        routing_key = message.routing_key
        raw_body = message.body.decode()
        data = json.loads(raw_body)

        if routing_key == "user.registered":
            user_registered_message = AmqpUserRegisteredMessage.parse_obj(data)
            await save_user(user_registered_message)
        elif routing_key == "user.book.view":
            user_book_view_message = AmqpUserBookViewMessage.parse_obj(data)
            await update_user_embedding(user_book_view_message)


async def user_consumer():
    QUEUE_USER = "pustakacerdas.user.queue"

    connection = await connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue(QUEUE_USER, durable=True)
    await queue.consume(handle_user_message)
