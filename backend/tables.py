from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)

    def __str__(self):
        return f"id:{self.id} name:{self.name} surname:{self.surname} birth_year:{self.birth_year}"


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(Integer, ForeignKey('authors.id'), index=True)
    isbn = Column(String, nullable=False)
    issue_year = Column(Integer, nullable=False)
    page_count = Column(Integer, nullable=False)

    author_rel = relationship('Author', backref='books')

    def __str__(self):
        return f"id:{self.id} name:{self.name} author_id:{self.author_id}" \
               f" isbn:{self.id} issue_year:{self.issue_year} page_count:{self.page_count}"
