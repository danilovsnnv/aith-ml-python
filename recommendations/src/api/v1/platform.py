from fastapi import APIRouter


router = APIRouter(tags=['platform'])

@router.get('/')
def index():
    return {'message': 'recommendation-service'}


@router.get('/healthcheck')
def healthcheck():
    return {'status': 'ok'}
