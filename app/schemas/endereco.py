from pydantic import BaseModel
from typing import Optional

class EnderecoBase(BaseModel):
    logradouro: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    id_tp_endereco: Optional[int] = None

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoRead(EnderecoBase):
    id: int
    id_usuario: int
    
    class Config:
        from_attributes = True
