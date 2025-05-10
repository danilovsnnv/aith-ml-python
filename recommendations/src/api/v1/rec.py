import numpy as np
import random
from fastapi import APIRouter, Request

from models import RecommendationsResponse, NewItemsEvent

router = APIRouter(prefix='/recs', tags=['recs'])

# unique_item_ids = set()
unique_item_ids = set([str(i) for i in range(100)])

EPSILON = 0.05

@router.get('/cleanup')
def cleanup():
    global unique_item_ids
    unique_item_ids = set()
    # try:
    #     redis_connection.delete('*')
    #     redis_connection.json().delete('*')
    # except redis.exceptions.ConnectionError:
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/add_items')
def add_movie(request: NewItemsEvent):
    global unique_item_ids
    for item_id in request.item_ids:
        unique_item_ids.add(item_id)


@router.get('/recs', response_model=RecommendationsResponse)
def get_recs(request: Request):
    global unique_item_ids

    # try:
    #     item_ids = redis_connection.json().get('top_items')
    # except redis.exceptions.ConnectionError:
    #     item_ids = None

    item_ids = None  # TODO: add recs
    user_id = request.headers.get('X-User-Id')

    if item_ids is None or random.random() < EPSILON:
        item_ids = np.random.choice(list(unique_item_ids), size=20, replace=False).tolist()
    return RecommendationsResponse(item_ids=item_ids)
