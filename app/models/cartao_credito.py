from sqlalchemy import Column, Date, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.core.sql_db import Base

class CartaoCredito(Base):
    __tablename__ = "cartao_credito"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(16), nullable=False, unique=True)
    dtExpiracao = Column(Date, nullable=False)
    cvv = Column(String(3), nullable=False)
    saldo = Column(DECIMAL(15, 2), nullable=False)
    id_usuario_cartao = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    
    usuario = relationship("Usuario", back_populates="cartoes")


    # @validates("numero")
    # def validar_numero(self,key,value):
    #     if not value.isdigit() or len(value) != 16:
    #         raise ValueError("Numero do cartão só pode ter 16 numeros, o cartão não foi criado")
    #     return value
    
    # @validates("cvv")
    # def validar_cvv(self,key,value):
    #     if not value.isdigit() or len(value) != 3:
    #         raise ValueError("O cvv só pode ter 3 numeros, o cartão não foi criado")
    
    
    
