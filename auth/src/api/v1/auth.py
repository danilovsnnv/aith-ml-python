from fastapi import APIRouter, Depends, HTTPException, status, Response

from core.config import settings
from core.dependencies import get_database_manager
from core.security import create_access_token
from schemas.user import SignInSchema, SignUpSchema
from services.database_manager import DatabaseManager

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(
    response: Response,
    sign_up: SignUpSchema,
    db_manager: DatabaseManager = Depends(get_database_manager)
):
    if db_manager.username_exists(sign_up.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already registered',
        )
    user_id = db_manager.add_user(sign_up.username, sign_up.password)
    access_token = create_access_token({'sub': str(user_id)})
    response.set_cookie(
        key=settings.cookie_name,
        value=access_token,
        httponly=True,
        secure=False,
        max_age=settings.cookie_max_age,
        samesite='lax'
    )
    return {'message': 'Registration successful'}


@router.post('/login')
def login(
    response: Response,
    sign_in: SignInSchema,
    db_manager: DatabaseManager = Depends(get_database_manager),
):
    user_id = db_manager.auth_user(sign_in.username, sign_in.password)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
        )
    access_token = create_access_token({'sub': str(user_id)})
    response.set_cookie(
        key=settings.cookie_name,
        value=access_token,
        httponly=True,
        secure=False,
        max_age=settings.cookie_max_age,
        samesite='lax'
    )
    return {'message': 'Login successful'}
