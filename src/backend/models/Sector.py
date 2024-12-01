from models.BaseModel import BaseModel
from sqlalchemy import DateTime, Integer, String, event
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database.sectors import DEFAULT_SECTORS

class Sector(BaseModel):
    __tablename__ = "sectors"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    code_name: Mapped[str] = mapped_column(String(5), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

# SQLAlchemy event listener that runs after table creation
@event.listens_for(Sector.__table__, 'after_create')
def insert_default_sectors(target, connection, **kw):
    for sector in DEFAULT_SECTORS:
        code_name = ''.join(word[0].upper() for word in sector['name'].split())[:5]
        connection.execute(
            target.insert().values(
                name=sector['name'],
                description=sector['description'],
                code_name=code_name
            )
        )
