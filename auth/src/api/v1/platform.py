from fastapi import APIRouter


router = APIRouter(tags=['platform'])

@router.get('/')
def index():
    return {'message': 'user service'}

@router.get('/healthcheck')
async def healthcheck():
    return {'status': 'ok'}
