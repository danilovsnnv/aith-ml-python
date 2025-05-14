import asyncio
import contextlib
import json
import logging
from pathlib import Path
from typing import cast, IO
import aio_pika
import polars as pl

from core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(filename='./logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MessageCollector:
    def __init__(
        self,
        queue_url: str,
        queue_name: str,
        routing_key: str,
        update_time: int = 10,
        prefetch_count: int = 10
    ):
        self.queue_url = queue_url
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.update_time = float(update_time)
        self.prefetch_count = prefetch_count

        self.buffer = []
        self.file_path = Path(__file__).resolve().parent.parent / 'data' / 'interactions.csv'
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_exists = self.file_path.exists()

        self.connection = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            settings.rabbitmq_url,
            loop=asyncio.get_event_loop()
        )

    async def _flush_buffer(self):
        if not self.buffer:
            logger.info('Buffer is empty. Nothing to flush.')
            return

        logger.info(f'Buffer has {len(self.buffer)} items. Starting to flush.')
        df = pl.DataFrame(self.buffer).rename({
            'item_id': 'item_ids',
            'action': 'actions'
        })

        write_header = not self.file_path.exists()
        with self.file_path.open('ab') as fp:
            df.write_csv(fp, has_header=write_header)

        self.file_exists = True
        self.buffer.clear()

        logger.info(f'Successfully flushed buffer.')

    async def _periodic_flusher(self):
        while True:
            await asyncio.sleep(self.update_time)
            await self._flush_buffer()

    async def collect(self):
        await self.connect()
        async with self.connection:
            channel = await self.connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(
                self.queue_name,
                durable=True,
                passive=True,
            )
            exchange = await channel.declare_exchange(
                settings.rabbitmq_exchange,
                durable=True,
                type='direct',
                passive=True,
            )
            await queue.bind(exchange, self.routing_key)

            flusher_task = asyncio.create_task(self._periodic_flusher())
            try:
                async with queue.iterator() as queue_iter:
                    logger.info(f'Start collecting messages from queue')
                    async for message in queue_iter:
                        async with message.process():
                            body = message.body.decode()
                            msg_dict = json.loads(body)
                            self.buffer.append(msg_dict)
            finally:
                flusher_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await flusher_task
                await self._flush_buffer()
