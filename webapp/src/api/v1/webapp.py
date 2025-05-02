import logging
import os
import requests
import uuid

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# Ensure logs directory exists
os.makedirs('/logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("/logs/router.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_url(host: str, port: str | int):
    if not host or not port:
        raise RuntimeError("Service host and port must be set via REC_SERVICE_HOST and REC_SERVICE_PORT")
    return f'http://{host}:{port}'

REC_SERVICE_URL = get_url(os.getenv('REC_SERVICE_HOST'), os.getenv('DEFAULT_PORT'))
INTERACTION_URL = get_url(os.getenv('INTERACTION_SERVICE_HOST'), os.getenv('DEFAULT_PORT'))

# TODO: remove this code
def get_imdb_url(imdb_id):
    str_imdb_id = str(imdb_id)
    return 'https://www.imdb.com/title/tt' + '0' * (7 - len(str_imdb_id)) + str_imdb_id

def fetch_items_data_for_item_ids(item_ids):
    return [
        {
            "item_id": item_id,
            "imdb_url": get_imdb_url(item_id),
            "image_filename": f"{item_id}.jpg",
            "title": f'Movie №{item_id}'
        }
        for item_id in item_ids if item_id
    ][:12]

@router.get("/")
async def index(request: Request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        user_id = request.session.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            request.session['user_id'] = user_id

    logger.info(f"Fetching recommendations for user_id={user_id}")
    logger.info(f"REC_SERVICE_URL={REC_SERVICE_URL}")
    recommendations_url = f"{REC_SERVICE_URL}/recs/{user_id}"
    response = requests.get(recommendations_url, timeout=60)
    if response.status_code == 200:
        recommended_item_ids = response.json().get('item_ids', [])
    else:
        recommended_item_ids = []

    items_data = fetch_items_data_for_item_ids(recommended_item_ids)


    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'items_data': items_data, 'interactions_url': INTERACTION_URL}
    )
