from typing import List
from sqlalchemy import insert, select
from models.tags import Tag
from models.task_tag_association import association_table
from schemas.tag import TagBase
from db.db import async_session


class TagRepository:

    @classmethod
    async def create_tag(cls, request: TagBase, user_id: int) -> TagBase:
        request_dict = request.model_dump()
        async with async_session() as session:
            stmt = insert(Tag).values(**request_dict, owner_id=user_id).returning(Tag)
            res = await session.execute(stmt)
            await session.commit()
            result = res.scalar_one()
            return TagBase.model_validate(result, from_attributes=True)

    @classmethod
    async def get_tags(cls, user_id: int) -> List[TagBase]:
        async with async_session() as session:
            stmt = select(Tag).where(Tag.owner_id == user_id)
            res = await session.execute(stmt)
            res = res.scalars().all()
            result = [
                TagBase.model_validate(task, from_attributes=True) for task in res
            ]
            return result

    @classmethod
    async def set_tags(cls, tag_id: int, task_id: int) -> None:
        async with async_session() as session:
            stmt = insert(association_table).values(task_id=task_id, tag_id=tag_id)
            await session.execute(stmt)
            await session.flush()
            await session.commit()
