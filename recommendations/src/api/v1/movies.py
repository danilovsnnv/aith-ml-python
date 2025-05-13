from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import get_database_manager
from schemas.movies import MovieIn, MovieOut
from services.database_manager import MovieDatabaseManager

router = APIRouter(prefix='/movies', tags=['movies'])


@router.post('/movies/', response_model=MovieOut)
async def create_movie(
    movie: MovieIn,
    db_manager: MovieDatabaseManager = Depends(get_database_manager)
):
    movie_id: int | None = db_manager.add_movie(**movie.model_dump())
    if not movie_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Error adding movie')
    return {'message': f'Movie "{movie_id}" added to database'}


@router.get('/movies/{movie_id}', response_model=MovieOut)
async def read_movie(
    movie_id: int,
    db_manager: MovieDatabaseManager = Depends(get_database_manager)
) -> MovieOut:
    movie: MovieOut | None = db_manager.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Movies not found')
    return movie
