import pytest
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models.Sector import Sector
from app import app
from configs.dependencies import get_session
from models.BaseModel import BaseModel
import asyncpg
import asyncio

# Test database URL and connection parameters
DB_USER = "root"
DB_PASS = "root"
DB_HOST = "localhost"
DB_NAME = "test_ellp_db"
TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

async def create_database():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        database="postgres"
    )
    
    # Drop database if exists and create new one
    await conn.execute(f'DROP DATABASE IF EXISTS {DB_NAME}')
    await conn.execute(f'CREATE DATABASE {DB_NAME}')
    await conn.close()

async def drop_database():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        database="postgres"
    )
    
    await conn.execute(f'DROP DATABASE IF EXISTS {DB_NAME}')
    await conn.close()

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    asyncio.run(create_database())
    yield
    asyncio.run(drop_database())

@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
    )
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    async with async_session() as session:
        # Create a test sector
        sector = Sector(
            name="Technology",
            description="Tech department",
            code_name="TECH"
        )
        session.add(sector)
        await session.commit()
        
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

@pytest.fixture
async def client(async_session: AsyncSession) -> AsyncGenerator[TestClient, None]:
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_session
        
    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def volunteer_data():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "student_code": "12345",
        "sector": {
            "name": "Technology"
        }
    }