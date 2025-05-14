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

async def train_model_periodically(train_interval: int = 3600, filepath: str = 'data/interactions.csv'):
    while True:
        await asyncio.sleep(settings.update_time)
        df = pl.read_csv(filepath, has_header=True)
        train_item2vec(df)

async def main():
    await asyncio.gather(
        message_collector.collect(),
        train_model_periodically(3600)  # Every hour
    )

if __name__ == "__main__":
    asyncio.run(main())
async def main():
    await asyncio.gather(
        message_collector.collect(),
    )


if __name__ == '__main__':
    asyncio.run(main())
