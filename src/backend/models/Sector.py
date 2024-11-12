from models.BaseModel import BaseModel
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Sector(BaseModel):
    __tablename__ = "sectors"
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    code_name: Mapped[str] = mapped_column(String(5), nullable=False)
