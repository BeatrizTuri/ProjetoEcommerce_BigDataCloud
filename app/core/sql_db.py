import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

MYSQL_SSL_CA = os.getenv("MYSQL_SSL_CA")

# Cria a engine com SSL ativado
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {"ca": MYSQL_SSL_CA}
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
