from typing import Annotated
from fastapi import Depends
import fastapi_users
from fastapi_users.authentication import authenticator
from auth.manager import get_user_manager
from auth.auth import auth_backend
from models.users import User
from repositories.tag import TagRepository
from repositories.task import TaskRepository
from services.tag import TagService
from services.task import TaskService

task_repository = TaskRepository()
tag_repository = TagRepository()


tag_service = TagService(tag_repository)
task_service = TaskService(task_repository)



def get_tag_service():
    return tag_service

def get_task_service():
    return task_service



task_service_dependency = Annotated[dict, Depends(get_task_service)]
tag_service_dependency = Annotated[dict, Depends(get_tag_service)]



fastapi_users = fastapi_users.FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)