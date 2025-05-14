import asyncio

from core.config import settings
from services.message_collector import MessageCollector

message_collector = MessageCollector(
    queue_url=settings.rabbitmq_url,
    queue_name=settings.rabbitmq_queue,
    routing_key=settings.rabbitmq_routing_key,
    update_time=settings.update_time,
    prefetch_count=settings.prefetch_count
)

async def collect_messages():
    await message_collector.collect()


async def main():
    await asyncio.gather(
        message_collector.collect(),
    )


if __name__ == '__main__':
    asyncio.run(main())
