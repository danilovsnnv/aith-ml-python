# TODO: rewrite to *MoviesCatalog* service

from __future__ import annotations

import datetime
import logging
from contextlib import contextmanager
from typing import Any, Generator, Literal, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy import create_engine, exists
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from core.config import settings
from models.base import Base
from schemas.movies import MovieOut
from models.movies import Movies

ModelType = TypeVar('ModelType', bound=BaseModel)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(filename='./logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class MovieDatabaseManager:
    """
    Manager to work with movies database
    """
    def __init__(self):
        query_params = settings.query_params or {}
        db_url = URL(
            drivername="postgresql+psycopg2",
            username=settings.username,
            password=settings.password,
            host=settings.host,
            port=settings.port,
            database=settings.database,
            query=query_params,
        )

        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            logger.info(f'Database `{settings.database}` created successfully.')
        else:
            logger.info(f'Database `{settings.database}` already exists.')

        Base.metadata.create_all(self.engine)

    @contextmanager
    def _session_scope(self) -> Generator[Session, Any, None]:
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f'Error during working with session: {e}')
            raise
        finally:
            session.close()

    @staticmethod
    def _wrap_orm_object(
        wrap_type: Type[ModelType], obj: object
    ) -> ModelType:
        return wrap_type.model_validate(obj)

    @property
    def is_empty(self) -> bool:
        with self._session_scope() as session:
            return session.query(Movies).first() is None


    def add_movie(
        self,
        img_id: int,
        title_id: str,
        poster_url: str,
        item_type: Literal['Movies', 'Series'],
        name: str,
        original_name: str,
        description: str,
        genre: list[str],
        date: str,
        rating_count: float,
        rating_value: float,
        keywords: list[str],
        featured_review: str,
        stars: list[str],
        directors: list[str],
        creators: list[str],
    ) -> int:
        with self._session_scope() as session:
            new_movie = Movies(
                img_id=img_id,
                title_id=title_id,
                poster_url=poster_url,
                item_type=item_type,
                name=name,
                original_name=original_name,
                description=description,
                genre=genre,
                date=date,
                rating_count=rating_count,
                rating_value=rating_value,
                keywords=keywords,
                featured_review=featured_review,
                stars=stars,
                directors=directors,
                creators=creators
            )

            session.add(new_movie)
            session.flush()
            return new_movie.id

    def movie_exists(self, movie_id: int) -> bool:
        with self._session_scope() as session:
            return session.query(
                exists().where(Movies.id == movie_id)
            ).scalar()

    def title_exists(self, title: str) -> bool:
        with self._session_scope() as session:
            return session.query(
                exists().where(Movies.title_id == title)
            ).scalar()

    def get_movie(self, movie_id: int) -> MovieOut:
        with self._session_scope() as session:
            movie = session.get(Movies, movie_id)
            return self._wrap_orm_object(wrap_type=MovieOut, obj=movie)

    def get_top_rated_movies(self, n: int = 10) -> list[MovieOut]:
        with self._session_scope() as session:
            movies = (
                session.query(Movies)
                .order_by(
                    Movies.rating_value.desc().nullslast(),
                    Movies.rating_count.desc().nullslast()
                )
                .limit(n)
                .all()
            )
            return [
                self._wrap_orm_object(wrap_type=MovieOut, obj=movie)
                for movie in movies
            ]
