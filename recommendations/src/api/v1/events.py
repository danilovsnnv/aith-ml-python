import logging
import polars as pl
from fastapi import APIRouter

from core.dependencies import get_database_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=['events'])

@router.on_event('startup')
async def seed_movies():
    db_manager = get_database_manager()
    if not db_manager.is_empty:
        logger.debug('Database is not empty. Service will not add movies')
        return

    logger.debug('Database is empty. Adding movies to database')
    data = pl.read_parquet('data/movies.parquet')
    for row in data.rows(named=True):
        db_manager.add_movie(**row)
