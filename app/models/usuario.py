from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    email = Column(String(150))
    dtNascimento = Column(DateTime)
    CPF = Column(String(11))
    telefone = Column(String(20))
