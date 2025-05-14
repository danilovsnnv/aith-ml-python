import time
import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from models.events import InteractEvent
from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager
from core.dependencies import get_rabbitmq, get_redis, get_authorized_user_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/interact', tags=['interactions'])


@router.post('/interact')
async def interact(
    event: InteractEvent,
    user_id: str = Depends(get_authorized_user_id),
    watched_queue: RabbitMQManager = Depends(get_rabbitmq),
    watched_filter: RedisManager = Depends(get_redis),
):
    logger.info(f'Received interact from {user_id} to event: {event.action}')
    payload = event.model_dump()
    payload['user_id'] = user_id
    payload['timestamp'] = time.time()

    await watched_queue.publish(payload)
    watched_filter.add(user_id=user_id, item_id=event.item_id)

    return JSONResponse(content={'detail': 'published'}, status_code=200)
