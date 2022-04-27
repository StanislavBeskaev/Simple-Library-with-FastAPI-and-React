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
