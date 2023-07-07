from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/alembic"

Engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=Engine)


class Base(MappedAsDataclass, DeclarativeBase):
    pass
