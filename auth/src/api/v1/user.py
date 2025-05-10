from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from core.dependencies import get_authorized_user_id, get_database_manager
from models.balance import Balance, ChangeBalance
from models.responces import UserResponse
from services.database_manager import DatabaseManager

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/me', response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(get_authorized_user_id),
    database_manager: DatabaseManager = Depends(get_database_manager)
):
    user = database_manager.get_user(user_id)
    return user

@router.get('/check_balance', response_model=ChangeBalance)
def check_balance(
    user_id: int = Depends(get_authorized_user_id),
    db_manager: DatabaseManager = Depends(get_database_manager)
):
    account_balance: float | None = db_manager.get_balance(user_id)

    if account_balance is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={'WWW-Authenticate': 'Bearer'},
            content={'detail': 'Users not found.'},
        )

    return Balance(balance=account_balance)

@router.post('/change_balance')
def change_balance(
    user_id: int = Depends(get_authorized_user_id),
    db_manager: DatabaseManager = Depends(get_database_manager)
):
    change_amount = change_balance.balance_change
    account_balance: float | None = db_manager.change_balance(user_id, change_amount)
    
    if account_balance is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={'WWW-Authenticate': 'Bearer'},
            content={'detail': 'Users not found.'},
        )

    return {'message': 'Successfully changed user balance'}
