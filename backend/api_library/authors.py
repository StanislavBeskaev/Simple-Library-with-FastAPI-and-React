from fastapi import (
    APIRouter,
    Depends,
    status,
)

from backend import models
from backend.services.authors import AuthorsService
from backend.api_library.responses import authors as authors_responses


router = APIRouter(
    prefix='/authors',
    tags=['authors'],
)


@router.get(
    "/",
    response_model=list[models.Author],
    responses=authors_responses.get_authors_responses
)
def get_authors(authors_service: AuthorsService = Depends()):
    """Получение всех авторов"""
    return authors_service.get_many()


@router.post(
    "/",
    response_model=models.Author,
    status_code=status.HTTP_201_CREATED,
    responses=authors_responses.author_create_responses
)
def create_author(
        author_data: models.AuthorCreate,
        authors_service: AuthorsService = Depends()
):
    """Создание автора"""
    return authors_service.create(author_data=author_data)


@router.get(
    "/{author_id}",
    response_model=models.Author,
    responses=authors_responses.get_detail_author_responses
)
def get_author(author_id: int, authors_service: AuthorsService = Depends()):
    """Получение автора по id"""
    return authors_service.get(author_id=author_id)
