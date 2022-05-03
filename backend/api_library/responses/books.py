from ... import models
from . import HTTPError

get_books_responses = {
    200: {
        "description": "Информация о найденных книгах",
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
        }
    }
}

_book_detail_content = {
    "application/json": {
        "example": {
            "name": "Название книги",
            "author": 1,
            "isbn": "book_isbn",
            "issue_year": 1345,
            "page_count": 123,
            "id": 1
        }
    }
}

book_create_responses = {
    201: {
        "description": "Успешное создание книги",
        "content": _book_detail_content
    },
    400: {
        "model": models.BookValidationError,
        "description": "Ошибки валидации данных"
    }
}

_book_not_found_response = {
    "model": HTTPError,
    "description": "Книга не найдена",
    "content": {
        "application/json": {
            "example": {
                "detail": "Book with id 404 not found"
            }
        }
    }
}

get_detail_book_responses = {
    200: {
        "description": "Информация о книге",
        "content": _book_detail_content
    },
    404: _book_not_found_response
}

book_delete_responses = {
    204: {
        "description": "Успешное удаление книги",
        "content": {
            "application/json": {
                "example": None
            }
        }
    },
    404: _book_not_found_response
}

book_update_responses = {
    200: {
        "description": "Книга успешно изменена",
        "content": _book_detail_content
    },
    400: {
        "model": models.BookValidationError,
        "description": "Ошибки валидации данных"
    },
    404: _book_not_found_response
}
