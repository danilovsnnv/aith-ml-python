import time
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.events import InteractEvent
from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager
from core.dependencies import get_rabbitmq, get_redis, get_authorized_user_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('./logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/interact', tags=['interactions'])


@router.post('/interact', status_code=200)
async def interact(
    event: InteractEvent,
    user_id: str = Depends(get_authorized_user_id),
    watched_queue: RabbitMQManager = Depends(get_rabbitmq),
    watched_filter: RedisManager = Depends(get_redis),
):
    logger.info(f'Received interact from user={user_id} action={event.action}')
    is_new = watched_filter.add(user_id=user_id, item_id=event.item_id)
    if not is_new:
        logger.debug(f'Duplicate interaction blocked for user={user_id}, item={event.item_id}')
        raise HTTPException(
            status_code=409,
            detail='Interaction already recorded'
        )

    # Only publish new interactions
    payload = event.model_dump()
    payload.update({
        'user_id': user_id,
        'timestamp': time.time(),
    })
    await watched_queue.publish(payload)

    return JSONResponse(content={'detail': 'published'}, status_code=200)
