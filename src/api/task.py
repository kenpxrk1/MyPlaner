import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends

from models.users import User
from repositories.task import TaskRepository
from schemas.task import TaskCreate, TaskRead
from api.dependencies import current_user, task_service_dependency
from services.task import TaskService




router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("", response_model=List[TaskRead])
async def get_all_tasks(
    service: task_service_dependency,
    current_user: User = Depends(current_user)
):
    all_tasks = await service.get_all_tasks(current_user.id)
    return all_tasks


@router.get("/{date}", response_model=List[TaskRead])
async def get_tasks_by_date(
    date: datetime.date,
    service: task_service_dependency,
    current_user: User = Depends(current_user)
):
    all_tasks = await service.get_tasks_by_date(current_user.id, date)
    return all_tasks


@router.post("", response_model=TaskCreate)
async def create_task(
    new_task: TaskCreate,
    service: task_service_dependency,
    current_user: User = Depends(current_user),
):
    task = await service.create_task(new_task, current_user.id)
    return task



