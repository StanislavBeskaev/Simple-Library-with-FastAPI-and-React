from fastapi import (
    APIRouter,
    Depends,
    status,
)

from .. import models
from ..services.authors import AuthorsService


router = APIRouter(
    prefix='/authors',
    tags=['authors'],
)


# TODO пример
@router.get(
    "/",
    response_model=list[models.Author]
)
def get_authors(authors_service: AuthorsService = Depends()):
    """Получение всех авторов"""
    return authors_service.get_many()


@router.post(
    "/",
    response_model=models.Author,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Успешное создание автора",
            "content": {
                "application/json": {
                    "example": {
                          "name": "Имя автора",
                          "surname": "Фамилия автора",
                          "birth_year": 1234,
                          "id": 1
                    }
                }
            }
        },
        400: {
            "model": models.AuthorCreateValidationError,
            "description": "Ошибки валидации данных"
        }
    }
)
def create_author(
        author_data: models.AuthorCreate,
        authors_service: AuthorsService = Depends()
):
    """Создание автора"""
    return authors_service.create(author_data=author_data)


# TODO пример
@router.get(
    "/{author_id}",
    response_model=models.Author
)
def get_author(author_id: int, authors_service: AuthorsService = Depends()):
    """Получение автора по id"""
    return authors_service.get(author_id=author_id)
