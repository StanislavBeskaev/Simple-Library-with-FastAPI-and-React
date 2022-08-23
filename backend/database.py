from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.settings import get_settings


engine = create_engine(get_settings().sqlalchemy_connection_url)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    logger.debug("call get_session")
    session = Session()
    try:
        yield session
    finally:
        session.close()

