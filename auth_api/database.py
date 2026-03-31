from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Conecta no banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Abre conexão por requisição
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Cria uma base dos modelos
Base = declarative_base()

