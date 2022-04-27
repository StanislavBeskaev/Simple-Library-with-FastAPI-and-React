from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import JSONResponse

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


@router.post(
    "/",
    response_model=models.Book
)
def create_book(
        book_data: models.BookCreate,
        books_service: BooksService = Depends()
):
    """Создание книги"""
    return books_service.create(book_data=book_data)


@router.get(
    "/{book_id}",
    response_model=models.Book
)
def get_book(book_id: int, books_service: BooksService = Depends()):
    """Получение книги по id"""
    return books_service.get(book_id=book_id)


@router.delete(
    "/{book_id}"
)
def delete_book(book_id: int, books_service: BooksService = Depends()):
    """Удаление книги по id"""
    books_service.delete(book_id=book_id)

    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{book_id}",
    response_model=models.Book
)
def update_book(
        book_id: int,
        book_data: models.BookUpdate,
        books_service: BooksService = Depends()
):
    return books_service.update(book_id=book_id, book_data=book_data)
