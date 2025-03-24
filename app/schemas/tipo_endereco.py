from pydantic import BaseModel

class TipoEnderecoBase(BaseModel):
    tipo: str  # Apenas o nome do tipo de endereço

class TipoEnderecoCreate(TipoEnderecoBase):
    pass  # Usado ao criar um novo tipo de endereço

class TipoEnderecoRead(TipoEnderecoBase):
    id: int  # Inclui o ID ao retornar um tipo de endereço

    class Config:
        from_attributes = True  # Permite conversão automática do SQLAlchemy
