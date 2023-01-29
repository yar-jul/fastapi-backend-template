from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from api.config.settings import settings


def get_sessionmaker():
    engine: AsyncEngine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_DSN,
        poolclass=NullPool,
        echo=settings.SQLALCHEMY_LOG_ALL,
    )
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
