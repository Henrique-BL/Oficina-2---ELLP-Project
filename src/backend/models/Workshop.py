from models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Workshop(BaseModel):
    __tablename__ = "workshops"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    workload: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
