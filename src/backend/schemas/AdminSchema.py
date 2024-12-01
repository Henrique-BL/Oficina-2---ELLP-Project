from typing import Annotated
from pydantic import Field
from schemas.BaseSchema import BaseSchema, OutMixin

class AdminSchema(BaseSchema):
    name: Annotated[str, Field(description="Nome do setor")]
    email: Annotated[str, Field(description="Email do setor")]
    password: Annotated[str, Field(description="Senha do setor")]
    
class AdminInLogin(BaseSchema):
    email: Annotated[str, Field(description="Email do setor")]
    password: Annotated[str, Field(description="Senha do setor")]
     
class AdminInRegister(AdminSchema):
    pass
class AdminOutRegister(OutMixin, AdminSchema):
    pass
class AdminOut(OutMixin):
    name: Annotated[str, Field(description="Nome do setor")]
    email: Annotated[str, Field(description="Email do setor")]
