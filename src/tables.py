from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
