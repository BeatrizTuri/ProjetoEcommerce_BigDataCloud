from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.sql_db import Base

class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    dtNascimento = Column(DateTime, nullable=True)
    cpf = Column(String(11), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    
    #Descomentar linhas a baixo assim que as classes forem criadas
    cartoes = relationship("CartaoCredito", back_populates="usuario")
    # enderecos = relationship("Endereco", back_populates="usuario")
    # pedidos = relationship("Pedido", back_populates="usuario")
