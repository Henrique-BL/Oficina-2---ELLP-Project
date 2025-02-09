from typing import Annotated
from pydantic import Field
from schemas.BaseSchema import BaseSchema, OutMixin
from datetime import datetime

class WorkshopBaseSchema(BaseSchema):
    name: Annotated[str, Field(description="Nome do workshop")]
    date: Annotated[datetime, Field(description="Data do workshop")]
    description: Annotated[str, Field(description="Descrição do workshop")]
    workload: Annotated[str, Field(description="Carga horária do workshop")]
    is_active: Annotated[bool, Field(default=True, description="Status do workshop")]



class WorkshopIn(WorkshopBaseSchema):
    pass


class WorkshopOut(WorkshopIn, OutMixin):
    pass