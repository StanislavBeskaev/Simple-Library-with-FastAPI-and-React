from backend import models
from backend.api_library.responses import HTTPError

author_create_responses = {
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

get_authors_responses = {
    200: {
        "description": "Информация об авторах в библиотеке",
        "content": {
            "application/json": {
                "example": [
                    {
                        "name": "Автор",
                        "surname": "Первый",
                        "birth_year": 1,
                        "id": 1
                    },
                    {
                        "name": "Автор",
                        "surname": "Второй",
                        "birth_year": 2,
                        "id": 2
                    },
                    {
                        "name": "Александр",
                        "surname": "Пушкин",
                        "birth_year": 1799,
                        "id": 7
                    },
                ]
            }
        }
    }
}

get_detail_author_responses = {
    200: {
        "description": "Информация об авторе",
        "content": {
            "application/json": {
                "example": {
                    "name": "Александр",
                    "surname": "Пушкин",
                    "birth_year": 1799,
                    "id": 1
                }
            }
        }
    },
    404: {
        "model": HTTPError,
        "description": "Автор не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Author with id 404 not found"
                }
            }
        }
    }
}
