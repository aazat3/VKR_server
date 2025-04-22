from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer


# from pathlib import Path
import logging

from user_auth.auth import get_current_user, get_password_hash, authenticate_user, create_access_token
from SQL.users.dao import *


router = APIRouter(prefix='/auth', tags=['Auth'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register/")
async def register_user(user_data: UserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'} 

@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    users_access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=users_access_token, httponly=True)
    return {'users_access_token': users_access_token, 'refresh_token': None}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me/")
async def get_me(user_data: UserModel = Depends(get_current_user)):
# async def get_me(token: str = Depends(oauth2_scheme)):
#     user_data: UserModel = get_current_user(token)
    return user_data
