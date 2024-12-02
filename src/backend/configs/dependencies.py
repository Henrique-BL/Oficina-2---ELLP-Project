from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from configs.database import get_session, get_test_session      

DataBaseDependency = Annotated[AsyncSession, Depends(get_session)]
DataBaseTestDependency = Annotated[AsyncSession, Depends(get_test_session)]