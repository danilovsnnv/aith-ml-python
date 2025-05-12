from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from core.dependencies import get_authorized_user_id, get_database_manager
from schemas.balance import Balance, ChangeBalance
from schemas.users import UserResponse
from services.database_manager import AuthDatabaseManager

router = APIRouter(prefix='/profile', tags=['profiles'])

@router.get('/me', response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(get_authorized_user_id),
    database_manager: AuthDatabaseManager = Depends(get_database_manager)
):
    user = database_manager.get_user(user_id)
    return user

@router.get('/check_balance', response_model=ChangeBalance)
def check_balance(
    user_id: int = Depends(get_authorized_user_id),
    db_manager: AuthDatabaseManager = Depends(get_database_manager)
):
    if not db_manager.user_exists(user_id):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={'WWW-Authenticate': 'Bearer'},
            content={'detail': f'Users with id={id} found.'},
        )

    account_balance: float = db_manager.get_balance(user_id)

    return Balance(balance=account_balance)

@router.post('/change_balance')
def change_balance(
    change_form: ChangeBalance = Body(...),
    user_id: int = Depends(get_authorized_user_id),
    db_manager: AuthDatabaseManager = Depends(get_database_manager)
):
    if not db_manager.user_exists(user_id):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            headers={'WWW-Authenticate': 'Bearer'},
            content={'detail': f'Users with id={id} found.'},
        )

    account_balance: float | None = db_manager.change_balance(user_id, change_form.balance_change)
    
    if account_balance is None:
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            headers={'WWW-Authenticate': 'Bearer'},
            content={'detail': 'Not enough money to perform operation'},
        )

    return {'message': 'Successfully changed user balance'}
