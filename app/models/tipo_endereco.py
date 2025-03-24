from sqlalchemy import Column, Integer, String
from app.core.sql_db import Base
from sqlalchemy.orm import relationship

class TipoEndereco(Base):
    __tablename__ = "tipo_endereco"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(45), nullable=False)

    enderecos = relationship("Endereco", back_populates="tipo_endereco")