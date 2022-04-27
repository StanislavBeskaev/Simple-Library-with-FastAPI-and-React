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


@router.get(
    "/",
    response_model=list[models.Author]
)
def get_authors(authors_service: AuthorsService = Depends()):
    """Получение всех авторов"""
    return authors_service.get_many()


# TODO описать 400 код ответа при ошибках валидации
@router.post(
    "/",
    response_model=models.Author,
    status_code=status.HTTP_201_CREATED
)
def create_author(
        author_data: models.AuthorCreate,
        authors_service: AuthorsService = Depends()
):
    """Создание автора"""
    return authors_service.create(author_data=author_data)
