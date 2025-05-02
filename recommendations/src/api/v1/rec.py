import numpy as np
import random
import redis
from fastapi import APIRouter

from models import InteractEvent, RecommendationsResponse, NewItemsEvent
from services.watched_filter import WatchedFilter

router = APIRouter(tags=['recs'])

redis_connection = redis.Redis('localhost')
watched_filter = WatchedFilter()

# unique_item_ids = set()
unique_item_ids = set([str(i) for i in range(100)])

EPSILON = 0.05

@router.get('/')
def index():
    return {'message': 'recommendation-service'}

@router.get('/healthcheck')
def healthcheck():
    return 200


@router.get('/cleanup')
def cleanup():
    global unique_item_ids
    unique_item_ids = set()
    try:
        redis_connection.delete('*')
        redis_connection.json().delete('*')
    except redis.exceptions.ConnectionError:
        pass
    return 200


@router.post('/add_items')
def add_movie(request: NewItemsEvent):
    global unique_item_ids
    for item_id in request.item_ids:
        unique_item_ids.add(item_id)
    return 200


@router.get('/recs/{user_id}')
def get_recs(user_id: str):
    global unique_item_ids

    try:
        item_ids = redis_connection.json().get('top_items')
    except redis.exceptions.ConnectionError:
        item_ids = None

    if item_ids is None or random.random() < EPSILON:
        item_ids = np.random.choice(list(unique_item_ids), size=20, replace=False).tolist()
    return RecommendationsResponse(item_ids=item_ids)


@router.post('/interact')
async def interact(request: InteractEvent):
    watched_filter.add(request.user_id, request.item_ids)
    return 200