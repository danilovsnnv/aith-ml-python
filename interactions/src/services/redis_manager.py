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
        logging.FileHandler("./logs/app.log"),
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

    def add(self, user_id: id_type, item_id: id_type) -> bool:
        """
        Помечает item_id просмотренным пользователем user_id.
        Возвращает True, если был добавлен новый элемент.
        """
        try:
            key = self._key(user_id)
            added = self.redis.sadd(key, item_id)
            if self.ttl:
                self.redis.expire(key, self.ttl)
            return bool(added)
        except RedisError as e:
            logger.error(f'Error during adding elements for {key=} and {item_id=}: {e}', exc_info=True)
            return False

    def remove(self, user_id: id_type, item_id: id_type) -> bool:
        """
        Убирает конкретный item_id из просмотренных для user_id.
        """
        try:
            key = self._key(user_id)
            return self.redis.srem(key, item_id) == 1
        except RedisError as e:
            logger.error(f'Error during removing elements for {key=} and {item_id=}: {e}', exc_info=True)
            return False

    def get(self, user_id: id_type) -> bytes | None:
        """
        Возвращает список всех просмотренных item_id для user_id.
        """
        try:
            key = self._key(user_id)
            return self.redis.get(key)
        except redis.exceptions.ConnectionError as e:
            logger.error(f'Error during removing elements for {key=}: {e}', exc_info=True)
            return None
