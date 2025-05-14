from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any, Generator, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import create_engine, exists
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from core.config import settings
from core.security import get_password_hash, verify_password
from models.base import Base
from schemas.users import UserResponse
from models.users import Users

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


class AuthDatabaseManager:
    """
    Manager to work with database
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
            raise e
        finally:
            session.close()

    @staticmethod
    def _wrap_orm_object(
        wrap_type: Type[ModelType], obj: object
    ) -> ModelType:
        return wrap_type.model_validate(obj)

    def add_user(
        self,
        username: str,
        password: str,
    ) -> int:
        with self._session_scope() as session:
            password_hash = get_password_hash(password)
            new_user = Users(
                username=username,
                password_hash=password_hash,
                balance=0,
                user_metadata={}
            )
            session.add(new_user)
            session.flush()
            return new_user.id

    def user_exists(self, user_id: int) -> bool:
        with self._session_scope() as session:
            return session.query(
                exists().where(Users.id == user_id)
            ).scalar()

    def username_exists(self, username: str) -> bool:
        with self._session_scope() as session:
            return session.query(
                exists().where(Users.username == username)
            ).scalar()

    def get_user(self, user_id: int) -> UserResponse:
        with self._session_scope() as session:
            user = session.get(Users, user_id)
            return self._wrap_orm_object(wrap_type=UserResponse, obj=user)

    def auth_user(self, username, password) -> int | None:
        with self._session_scope() as session:
            user = session.query(Users).filter_by(username=username).first()
            if not user or not verify_password(password, user.password_hash):
                return None

            return user.id

    def get_balance(self, user_id: int) -> float:
        with self._session_scope() as session:
            user = session.query(Users).filter_by(id=user_id).first()
            return user.balance

    def change_balance(self, user_id: int, change_amount: float) -> float | None:
        with self._session_scope() as session:
            user = session.query(Users).filter_by(id=user_id).first()

            if user.balance + change_amount < 0:
                return None

            user.balance += change_amount
            return user.balance
