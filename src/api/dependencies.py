from typing import Annotated
from fastapi import Depends
import fastapi_users
from fastapi_users.authentication import authenticator
from auth.manager import get_user_manager
from auth.auth import auth_backend
from models.users import User
from repositories.task import TaskRepository
from services.task import TaskService

task_repository = TaskRepository()
task_service = TaskService(task_repository)

def get_task_service():
    return task_service

task_service_dependency = Annotated[dict, Depends(get_task_service)]

fastapi_users = fastapi_users.FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)