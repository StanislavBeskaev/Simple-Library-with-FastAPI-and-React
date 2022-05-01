from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field


class BaseBook(BaseModel):
    name: str = Field(..., title="Название")
    author: int = Field(..., title="Id автора")
    isbn: str = Field(..., title="ISBN")
    issue_year: int = Field(..., title="Год выпуска")
    page_count: int = Field(..., title="Количество страниц")


class BookCreate(BaseBook):
    pass


class BookUpdate(BaseBook):
    pass


class Book(BaseBook):
    id: int = Field(..., title="Id книги")

    class Config:
        orm_mode = True


class BookSearchResult(BaseModel):
    count: int = Field(..., title="Количество найденных книг")
    results: list[Book] = Field(..., title="Найденные книги")


@dataclass
class BookSearchParam:
    name: str | None = Query(None, description="Строка в названии книги(без учёта регистра)")
    issue_year_gte: int | None = Query(None, alias="issue_year__gte", description="Год выпуска от")
    issue_year_lte: int | None = Query(None, alias="issue_year__lte", description="Год выпуска до")
    page_count_gte: int | None = Query(None, alias="page_count__gte", description="Количество страниц в книге от")
    page_count_lte: int | None = Query(None, alias="page_count__lte", description="Количество страниц в книге до")
    author: int | None = Query(None, description="Id автора")
    page: int = Query(1, description="Номер страницы")
    page_size: int = Query(20, description="Количество книг на странице")
