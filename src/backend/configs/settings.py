from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_URL: str = Field(default="postgresql+asyncpg://root:root@localhost/ellp_db")
    TEST_DB_URL: str = Field(default="postgresql+asyncpg://root:root@localhost/test_ellp_db")
    

settings = Settings()