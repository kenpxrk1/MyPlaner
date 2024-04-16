from fastapi import FastAPI
from contextlib import asynccontextmanager
from auth.auth import auth_backend
import fastapi_users

from auth.manager import get_user_manager
from models.users import User
from schemas.user import UserCreate, UserRead
from api.routers import all_routers




app = FastAPI(
    title="MyPlaner: Sira",
)

fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

for router in all_routers:
    app.include_router(router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

