from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{settings.pg_host}:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

