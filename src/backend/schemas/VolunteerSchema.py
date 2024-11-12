from typing import Annotated
from pydantic import Field
from schemas.BaseSchema import BaseSchema, OutMixin
from schemas.SectorSchema import SectorIn

class VolunteerBaseSchema(BaseSchema):
    name: Annotated[str, Field(description="Nome do voluntário")]
    email: Annotated[str, Field(description="Email do voluntário")]
    phone: Annotated[str, Field(description="Telefone do voluntário")]
    student_code: Annotated[str, Field(description="Código de estudante do voluntário")]
    sector: Annotated[SectorIn, Field(description="Setor do voluntário")]
    
class VolunteerIn(VolunteerBaseSchema):
    pass

class VolunteerOut(VolunteerIn, OutMixin):
    pass