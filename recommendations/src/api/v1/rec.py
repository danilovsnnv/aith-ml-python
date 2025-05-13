import logging
from fastapi import APIRouter, Depends

from core.dependencies import get_database_manager, get_authorized_user_id
from schemas.recommendations import RecommendationResponse
from services.database_manager import MovieDatabaseManager

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


@router.get('/recs', response_model=list[RecommendationResponse])
def get_recs(
    user_id: str = Depends(get_authorized_user_id),
    db_manager: MovieDatabaseManager = Depends(get_database_manager),
) -> list[RecommendationResponse]:
    # TODO: add cold start check
    logger.info(f'Getting recs for {user_id}')
    movies = db_manager.get_top_rated_movies(n=20)
    return [movie.to_recommendation_response() for movie in movies]

