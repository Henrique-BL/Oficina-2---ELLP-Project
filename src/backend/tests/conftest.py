import pytest
import pytest_asyncio
from app import app
from configs.dependencies import get_session, get_test_session
from models.BaseModel import BaseModel
import asyncpg
from configs.settings import settings
from fastapi.testclient import TestClient
DB_NAME = "test_ellp_db"


async def create_database():
    conn = await asyncpg.connect(settings.TEST_DB_URL.replace("test_ellp_db", "postgres").replace("postgresql+asyncpg", "postgresql"))
    try:
        await conn.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
        await conn.execute(f'DROP DATABASE IF EXISTS {DB_NAME}')
        await conn.execute(f'CREATE DATABASE {DB_NAME}')
    finally:
        await conn.close()
        

async def drop_database():
    conn = await asyncpg.connect(settings.TEST_DB_URL.replace("test_ellp_db", "postgres").replace("postgresql+asyncpg", "postgresql"))
    try:
        await conn.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{DB_NAME}'
            AND pid <> pg_backend_pid()
        """)
        await conn.execute(f'DROP DATABASE IF EXISTS {DB_NAME}')
    finally:
        await conn.close()

async def create_tables(db_session):
    async for session in db_session:
        async with session.begin(): await session.run_sync(lambda sync_session: BaseModel.metadata.create_all(sync_session.connection()))

@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_test_database():
    print('Creating database')
    await create_database()
    print('Creating tables')
    await create_tables(get_test_session())
    yield
    print('Dropping database')
    await drop_database()

    
@pytest_asyncio.fixture(scope="session")
async def client_test():
    app.dependency_overrides.clear()
    app.dependency_overrides[get_session] = get_test_session
    print('app', app.dependency_overrides[get_session])
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def volunteer_data():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "student_code": "12345",
        "is_active": True
    }
@pytest.fixture(scope="session")
def admin_data():
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "1234567890"
    }
@pytest.fixture(scope="session")
def sector_data():
    return {
        "name": "Technology",
        "description": "Tech department",
        "code_name": "tech"
    }
