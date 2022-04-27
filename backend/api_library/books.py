from fastapi import (
    APIRouter,
    Depends,
    status,
)

from .. import models
from ..services.books import BooksService


router = APIRouter(
    prefix='/books',
    tags=['books'],
)


# TODO параметры фильтрации
@router.get(
    "/",
    response_model=models.BookSearchResult
)
def get_books(books_service: BooksService = Depends()):
    """Получение книг"""
    return books_service.get_many()


@router.get(
    "/{book_id}",
    response_model=models.Book
)
def get_book(book_id: int, books_service: BooksService = Depends()):
    """Получение книги по id"""
    return books_service.get(book_id=book_id)
