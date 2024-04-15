from typing import Annotated
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import String, text
from config.config import settings
from models.base import Base
import datetime

from models.users import User




async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)




async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)