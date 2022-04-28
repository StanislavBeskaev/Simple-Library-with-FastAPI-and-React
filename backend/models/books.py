from pydantic import BaseModel, Field


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


class BookSearchParam(BaseModel):
    name: str | None
    issue_year_gte: int | None = Field(alias="issue_year__gte")
    issue_year_lte: int | None = Field(alias="issue_year__lte")
    page_count_gte: int | None = Field(alias="page_count__gte")
    page_count_lte: int | None = Field(alias="page_count__lte")
    author: int | None
    page: int = Field(1)
    page_size: int = Field(20)
