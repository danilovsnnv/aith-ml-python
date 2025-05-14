from __future__ import annotations

import logging
from typing import TypeAlias

import redis
from redis.exceptions import RedisError

from core.config import settings

id_type: TypeAlias = int | str

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(filename='./logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(
        self,
        db: int = 0,
        key_prefix: str = 'watched',
        ttl_seconds: int | None = None,
        redis_client: redis.Redis | None = None,
    ):
        self.prefix = key_prefix
        self.ttl = ttl_seconds

        if redis_client:
            self.redis = redis_client
        else:
            pool = redis.ConnectionPool(
                host=settings.redis_host,
                port=settings.redis_port,
                db=db,
                decode_responses=True,
                socket_keepalive=True,
            )
            self.redis = redis.Redis(connection_pool=pool)

    def _key(self, user_id: id_type) -> str:
        return f'{self.prefix}:{user_id}'

    def get(self, user_id: id_type) -> set[bytes]:
        """
        Возвращает список всех просмотренных item_id для user_id.
        """
        try:
            key = self._key(user_id)
            return self.redis.smembers(key) or set()
        except RedisError as e:
            logger.error(f'Error fetching watched set for {key=}: {e}', exc_info=True)
            return set()
