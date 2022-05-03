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


class BookValidationError(BaseModel):
    name: str = Field("Книга с таким названием уже существует", title="Ошибки валидации названия")
    isbn: str = Field("Книга с таким ISBN уже существует", title="Ошибки валидации ISBN")
    issue_year: str = Field("Год выпуска должен быть больше 0", title="Ошибки валидации года выпуска")
    page_count: str = Field("Количество страниц должно быть больше 0", title="Ошибки валидации количества страниц")
