from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.sql_db import Base

class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True, index=True)
    logradouro = Column(String(200), nullable=False)
    complemento = Column(String(200), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    id_tp_endereco = Column(Integer, ForeignKey("tipo_endereco.id"), nullable=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="enderecos")
    tipo_endereco = relationship("TipoEndereco", back_populates="enderecos")

