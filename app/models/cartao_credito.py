from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.sql_db import Base

class CartaoCredito(Base):
    __tablename__ = "cartao_credito"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(45), nullable=False, unique=True)
    dtExpiracao = Column(DateTime, nullable=False)
    cvv = Column(String(3), nullable=False)
    saldo = Column(DECIMAL(15, 2), nullable=False)
    id_usuario_cartao = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="cartoes")
