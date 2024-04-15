import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import text
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column



# class User(Base):
#     __tablename__ = "users"

#     user_id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(unique=True)
#     hashed_password: Mapped[str]
#     created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: bool
    is_superuser: bool
    is_verified: bool
    