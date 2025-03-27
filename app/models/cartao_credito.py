from sqlalchemy import Column, Date, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.core.sql_db import Base

class CartaoCredito(Base):
    __tablename__ = "cartao_credito"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, nullable=False, unique=True)
    dtExpiracao = Column(Date, nullable=False)
    cvv = Column(Integer, nullable=False)
    saldo = Column(DECIMAL(15, 2), nullable=False)
    id_usuario_cartao = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="cartoes")
