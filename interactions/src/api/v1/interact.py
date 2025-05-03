from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import time

from models.events import InteractEvent
from services.rabbitmq_manager import RabbitMQManager
from services.redis_manager import RedisManager
from core.dependences import get_rabbitmq, get_redis

router = APIRouter(tags=["interactions"])


@router.get("/")
async def index():
    return {"message": "interaction-service"}


@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@router.post("/interact")
async def interact(
    event: InteractEvent,
    watched_queue: RabbitMQManager = Depends(get_rabbitmq),
    watched_filter: RedisManager = Depends(get_redis),
):
    event.timestamp = time.time()

    await watched_queue.publish(event.model_dump())
    watched_filter.add(user_id=event.user_id, item_id=event.item_id)

    return JSONResponse(content={"detail": "published"}, status_code=200)


@router.on_event("startup")
async def _startup():
    await get_rabbitmq().connect()


@router.on_event("shutdown")
async def _shutdown():
    await get_rabbitmq().close()
