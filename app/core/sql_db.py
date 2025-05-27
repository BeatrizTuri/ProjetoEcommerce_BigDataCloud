import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_PATH = os.path.join(BASE_DIR, "..", "certs", "DigiCertGlobalRootCA.crt.pem")

engine = create_engine(
    DATABASE_URL,
    # connect_args={
    #     "ssl": {"ca": CERT_PATH}
    # }
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
