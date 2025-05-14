import logging
from fastapi import APIRouter, Depends, HTTPException

from core.dependencies import get_database_manager, get_redis_manager, get_authorized_user_id
from schemas.recommendations import RecommendationResponse
from services.database_manager import MovieDatabaseManager
from services.redis_manager import RedisManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/recs', tags=['recs'])


@router.get("/recs", response_model=list[RecommendationResponse])
def get_recs(
    user_id: str = Depends(get_authorized_user_id),
    db_manager: MovieDatabaseManager = Depends(get_database_manager),
    watched_filter: RedisManager = Depends(get_redis_manager),
) -> list[RecommendationResponse]:
    logger.info(f"Getting recs for user={user_id}")
    watched_str_ids = watched_filter.get(user_id)
    # template
    # if len(watched_str_ids) < 10:
    #     # cold start
    # else:
    #     # ML model
    logger.info(f"User's watched_str_ids={watched_str_ids}")
    watched_ids = {int(i) for i in watched_str_ids}
    movies = db_manager.get_top_rated_movies(n=20, exclude_ids=watched_ids)
    return [movie.to_recommendation_response() for movie in movies]
