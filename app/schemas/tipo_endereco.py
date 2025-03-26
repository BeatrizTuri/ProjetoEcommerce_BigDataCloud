from pydantic import BaseModel

class TipoEnderecoBase(BaseModel):
    tipo: str  

class TipoEnderecoCreate(TipoEnderecoBase):
    pass  

class TipoEnderecoRead(TipoEnderecoBase):
    id: int  

    class Config:
        from_attributes = True  
