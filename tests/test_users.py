from sqlalchemy import insert, select
from conftest import client, async_session_maker
from models.users import User
from src.models.tags import Tag


async def test_register():
    async with async_session_maker() as session:
        stmt = insert(User).values(email="lalala@mail.ru", 
                                   hashed_password="string",
                                   is_active=True,
                                   is_superuser=False,
                                   is_verified=False)
        await session.execute(stmt)
        await session.commit()
        query = select(User)
        result = await session.execute(query)
        assert result.all() != None


