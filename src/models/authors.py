from pydantic import BaseModel


class BaseAuthor(BaseModel):
    name: str
    surname: str
    birth_year: int


class AuthorCreate(BaseAuthor):
    pass


class Author(BaseAuthor):
    id: int

    class Config:
        orm_mode = True
