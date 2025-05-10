from fastapi import APIRouter

from core.dependencies import get_rabbitmq


router = APIRouter(tags=['events'])

@router.on_event('startup')
async def _startup():
    await get_rabbitmq().connect()


@router.on_event('shutdown')
async def _shutdown():
    await get_rabbitmq().close()
