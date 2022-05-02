from dataclasses import dataclass

from fastapi import Query


@dataclass
class BookSearchParam:
    name: str = Query(None, description="Строка в названии книги(без учёта регистра)")
    issue_year_gte: int = Query(None, alias="issue_year__gte", description="Год выпуска от")
    issue_year_lte: int = Query(None, alias="issue_year__lte", description="Год выпуска до")
    page_count_gte: int = Query(None, alias="page_count__gte", description="Количество страниц в книге от")
    page_count_lte: int = Query(None, alias="page_count__lte", description="Количество страниц в книге до")
    author: int = Query(None, description="Id автора")
    page: int = Query(1, description="Номер страницы")
    page_size: int = Query(20, description="Количество книг на странице")
