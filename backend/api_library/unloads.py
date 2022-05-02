from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import StreamingResponse

from .. import dependencies
from ..services.unloads import UnloadService


router = APIRouter(
    prefix='/unloads',
    tags=['unloads'],
)


@router.get("/authors")
def get_authors_unload(unloads_service: UnloadService = Depends()):
    """Получение json выгрузки авторов"""
    authors_unload = unloads_service.get_authors()

    return StreamingResponse(
        content=authors_unload,
        media_type="application/json",
        headers={'Content-Disposition': 'attachment; filename=authors.json'}
    )


@router.get("/books")
def get_books_unload(
        search_params: dependencies.BookSearchParam = Depends(),
        unloads_service: UnloadService = Depends()
):
    """Получение json выгрузки книг"""
    books_unload = unloads_service.get_books(search_params=search_params)

    return StreamingResponse(
        content=books_unload,
        media_type="application/json",
        headers={'Content-Disposition': 'attachment; filename=books.json'}
    )
