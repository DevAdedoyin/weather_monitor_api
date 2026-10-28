
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(
    settings.database_url
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# print("Database file:", Path(engine.url.database).resolve())

class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db

