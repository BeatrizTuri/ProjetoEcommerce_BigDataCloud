from pydantic import BaseModel
from typing import Optional
# from app.schemas.tipo_endereco import TipoEnderecoRead

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
    # tipo_endereco: Optional[TipoEnderecoRead] = None  # Retorna os detalhes do tipo de endereço
    
    class Config:
        from_attributes = True
