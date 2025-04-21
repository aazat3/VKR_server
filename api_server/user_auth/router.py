from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from jose import jwt, JWTError


# from pathlib import Path
import logging

from auth import *

from SQL.models import *
from SQL.users.schemas import *
from SQL.base_dao import *
from SQL.users.dao import *

from datetime import datetime, timezone

router = APIRouter(prefix='/auth', tags=['Auth'])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

# def get_token_from_cookie_or_header(
#     request: Request,
#     token_from_header: str = Depends(oauth2_scheme),
#     # users_access_token: str = Cookie(default=None, alias="users_access_token")
# ):
#     users_access_token = request.cookies.get('users_access_token')
#     # Приоритет: Cookie -> Header
#     token = users_access_token #or token_from_header
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
#     return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = Settings.get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


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
