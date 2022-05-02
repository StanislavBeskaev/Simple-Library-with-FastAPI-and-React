from pydantic import BaseModel, Field


class BaseAuthor(BaseModel):
    name: str = Field(..., title="Имя")
    surname: str = Field(..., title="Фамилия")
    birth_year: int = Field(..., title="Год рождения")


class AuthorCreate(BaseAuthor):
    pass


class Author(BaseAuthor):
    id: int = Field(..., title="Id")

    class Config:
        orm_mode = True


class AuthorCreateValidationError(BaseModel):
    name: str = Field("Автор с такими именем и фамилией уже существует", title="Ошибки валидации имени и фамилии")
    birth_year: str = Field("Год рождения должен быть больше 0", title="Ошибки валидации года рождения")
