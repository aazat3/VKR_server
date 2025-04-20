from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from SQL.models import *
from SQL.users.schemas import *
from SQL.users.dao import *
from SQL.base_dao import *



class UsersDAO(BaseDAO):
    model = UserModel
