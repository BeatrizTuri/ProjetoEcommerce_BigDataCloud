from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship
from app.core.sql_db import Base

class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    dtNascimento = Column(Date, nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    
    cartoes = relationship("CartaoCredito", back_populates="usuario", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="usuario",cascade="all,delete-orphan")
