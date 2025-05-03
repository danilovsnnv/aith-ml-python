from functools import lru_cache
from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager


@lru_cache()
def get_rabbitmq() -> RabbitMQManager:
    """
    В единственном экземпляре отдает RabbitMQ-сервис.
    """
    return RabbitMQManager()

@lru_cache()
def get_redis() -> RedisManager:
    """
    В единственном экземпляре отдает Redis сервис.
    """
    return RedisManager()
