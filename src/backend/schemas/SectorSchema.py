from typing import Annotated
from pydantic import Field
from datetime import datetime
from schemas.BaseSchema import BaseSchema, OutMixin

class SectorBaseSchema(BaseSchema):
    name: Annotated[str, Field(description="Nome do setor")]
    description: Annotated[str, Field(description="Descrição do setor")]
    code_name: Annotated[str, Field(description="Código do setor")]
    
class SectorIn(SectorBaseSchema):
    pass

class SectorOut(OutMixin, SectorBaseSchema):
    pass