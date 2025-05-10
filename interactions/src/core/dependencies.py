from fastapi import Header, HTTPException, status

from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager

rabbitmq_manager = RabbitMQManager()
redis_manager = RedisManager()


def get_rabbitmq() -> RabbitMQManager:
    """
    В единственном экземпляре отдает RabbitMQ-сервис.
    """
    return rabbitmq_manager


def get_redis() -> RedisManager:
    """
    В единственном экземпляре отдает Redis сервис.
    """
    return redis_manager


def get_authorized_user_id(x_user_id: int = Header(alias='X-User-Id')) -> int:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not authorized.'
        )

    return x_user_id
