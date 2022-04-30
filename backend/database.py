import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{os.environ.get('PG_HOST')}:5432/postgres"

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

