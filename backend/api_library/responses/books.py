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
        },
    },
}
