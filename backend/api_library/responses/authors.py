from ... import models


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
