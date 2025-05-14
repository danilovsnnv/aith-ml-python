import json

from aio_pika import connect_robust, Message, RobustConnection, RobustExchange
from core.config import settings


class RabbitMQManager:
    def __init__(self) -> None:
        self._connection: RobustConnection | None = None
        self._exchange: RobustExchange | None = None

    async def connect(self) -> None:
        if self._connection and not self._connection.is_closed:
            return

        self._connection = await connect_robust(settings.rabbitmq_url)
        channel = await self._connection.channel()
        self._exchange = await channel.declare_exchange(
            settings.rabbitmq_exchange,
            durable=True,
            type="direct",
        )

        queue = await channel.declare_queue(
            settings.rabbitmq_queue,
            durable=True,
        )
        await queue.bind(self._exchange, settings.rabbitmq_routing_key)

    async def publish(self, payload: dict) -> None:
        if not self._exchange:
            await self.connect()

        body = json.dumps(payload).encode("utf-8")
        message = Message(
            body,
            content_type="application/json",
        )
        await self._exchange.publish(message, routing_key=settings.rabbitmq_routing_key)

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
