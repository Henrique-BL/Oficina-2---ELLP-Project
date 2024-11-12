from typing import Annotated
from pydantic import Field
from schemas.BaseSchema import BaseSchema, OutMixin

class SectorBaseSchema(BaseSchema):
    name: Annotated[str, Field(description="Nome do setor")]

class SectorIn(SectorBaseSchema):
    pass

class SectorOut(SectorIn, OutMixin):
    pass
