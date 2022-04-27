from pydantic import BaseModel


class BaseBook(BaseModel):
    name: str
    author: int
    isbn: str
    issue_year: int
    page_count: int


class BookCreate(BaseBook):
    pass


class BookUpdate(BaseBook):
    pass


class Book(BaseBook):
    id: int

    class Config:
        orm_mode = True


class BookSearchResult(BaseModel):
    count: int
    results: list[Book]
