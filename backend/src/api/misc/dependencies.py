from typing import AsyncIterable

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def db_session(r: Request) -> AsyncIterable[AsyncSession]:
    async with r.app.state.db_session() as session:
        async with session.begin():
            yield session
