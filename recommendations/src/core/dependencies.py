from fastapi import HTTPException, Header, status

from services.database_manager import MovieDatabaseManager

database_manager = MovieDatabaseManager()

def get_database_manager() -> MovieDatabaseManager:
    return database_manager

def get_authorized_user_id(x_user_id: int = Header(alias='X-User-Id')) -> int:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not authorized.'
        )

    return x_user_id
