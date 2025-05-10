import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models.events import InteractEvent
from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager
from core.dependencies import get_rabbitmq, get_redis, get_authorized_user_id


router = APIRouter(prefix='/interact', tags=['interactions'])


@router.post('/interact')
async def interact(
    event: InteractEvent,
    user_id: str = Depends(get_authorized_user_id),
    watched_queue: RabbitMQManager = Depends(get_rabbitmq),
    watched_filter: RedisManager = Depends(get_redis),
):
    payload = event.model_dump()
    payload['user_id'] = user_id
    payload['timestamp'] = time.time()

    await watched_queue.publish(payload)
    watched_filter.add(user_id=user_id, item_id=event.item_id)

    return JSONResponse(content={'detail': 'published'}, status_code=200)
