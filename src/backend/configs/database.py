from configs.settings import settings 

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

async def get_test_session() -> AsyncGenerator:
    engine = create_async_engine(settings.TEST_DB_URL, echo = False)
    async_session = sessionmaker(
        engine, class_= AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def get_session() -> AsyncGenerator:
    engine = create_async_engine(settings.DB_URL, echo = False)

    async_session = sessionmaker(
        engine, class_= AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session