from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
)
from fastapi.responses import JSONResponse

from .. import models
from .. import dependencies
from ..services.books import BooksService


router = APIRouter(
    prefix='/books',
    tags=['books'],
)


@router.get(
    "/",
    response_model=models.BookSearchResult,
    responses={
        200: {
            "description": "Найденные книги",
            "content": {
                "application/json": {
                    "example": {
                        "count": 2,
                        "results": [
                            {
                                "name": "Тестовая книга 90241",
                                "author": 160,
                                "isbn": "test_isbn_90241",
                                "issue_year": 1505,
                                "page_count": 3,
                                "id": 90241
                            },
                            {
                                "name": "Тестовая книга 85886",
                                "author": 493,
                                "isbn": "test_isbn_85886",
                                "issue_year": 1569,
                                "page_count": 4,
                                "id": 85886
                            }
                        ]
                    }
                }
            },
        },
    },
)
def get_books(
        search_params: dependencies.BookSearchParam = Depends(),
        books_service: BooksService = Depends()
):
    """Получение книг"""
    return books_service.get_many(search_params=search_params)


# TODO описание 400 ответа и примеры
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


# TODO пример
@router.get(
    "/{book_id}",
    response_model=models.Book
)
def get_book(book_id: int = Path(..., description="Id книги"), books_service: BooksService = Depends()):
    """Получение книги по id"""
    return books_service.get(book_id=book_id)


# TODO описание 404 ответа и примеры
@router.delete(
    "/{book_id}"
)
def delete_book(book_id: int = Path(..., description="Id книги"), books_service: BooksService = Depends()):
    """Удаление книги по id"""
    books_service.delete(book_id=book_id)

    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


# TODO описание 406 ответа и примеры
@router.put(
    "/{book_id}",
    response_model=models.Book
)
def update_book(
        book_data: models.BookUpdate,
        book_id: int = Path(..., description="Id книги"),
        books_service: BooksService = Depends()
):
    """Обновление книги"""
    return books_service.update(book_id=book_id, book_data=book_data)
