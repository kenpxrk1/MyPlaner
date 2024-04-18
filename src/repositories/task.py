import datetime
from typing import List
from sqlalchemy import insert, select
from db.db import async_session
from models.tasks import Task
from schemas.task import TaskCreate, TaskRead
from sqlalchemy.orm import selectinload, joinedload


class TaskRepository:

    @classmethod
    async def create_task(cls, request: TaskCreate, owner_id: int) -> TaskRead:
        async with async_session() as session:
            request_dict = request.model_dump()
            stmt = (
                insert(Task).values(**request_dict, owner_id=owner_id).returning(Task)
            )

            res = await session.execute(stmt)
            await session.commit()
            result = res.scalar_one()
            return TaskCreate.model_validate(result, from_attributes=True)

    @classmethod
    async def get_all_tasks(cls, owner_id: int) -> List[TaskRead]:
        async with async_session() as session:
            stmt = (
                select(Task)
                .where(Task.owner_id == owner_id)
                .options(joinedload(Task.tags))
            )
            res = await session.execute(stmt)
            res = res.unique().scalars().all()
            result = [
                TaskRead.model_validate(task, from_attributes=True) for task in res
            ]
            return result

    @classmethod
    async def get_tasks_by_date(
        cls, owner_id: int, date: datetime.date
    ) -> List[TaskRead]:
        async with async_session() as session:
            stmt = (
                select(Task)
                .where(Task.owner_id == owner_id)
                .filter(Task.starts_at == date)
                .options(selectinload(Task.tags))
            )
            res = await session.execute(stmt)
            res = res.scalars().all()
            result = [
                TaskRead.model_validate(task, from_attributes=True) for task in res
            ]
            return result
