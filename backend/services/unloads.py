import json
from io import StringIO

from fastapi import Depends
from loguru import logger

from .. import models
from .authors import AuthorsService
from .books import BooksService


class UnloadService:
    """Сервис для выгрузки данных в json"""
    def __init__(self, books_service: BooksService = Depends(), authors_service: AuthorsService = Depends()):
        self.authors_service = authors_service
        self.books_service = books_service

    def get_authors(self) -> StringIO:
        """Получение выгрузки всех авторов"""
        logger.debug(f"Запрошена выгрузка авторов")

        authors = [models.Author.from_orm(author).dict() for author in self.authors_service.get_many()]

        output = StringIO()
        json.dump(obj=authors, fp=output, indent=2, ensure_ascii=False)
        output.seek(0)

        return output

    def get_books(self, search_params: models.BookSearchParam):
        """Получение выгрузки книг по переданным параметрам"""
        logger.debug(f"Запрошена выгрузка книг по параметрам: {search_params}")

        books = [models.Book.from_orm(book).dict()
                 for book in self.books_service.get_books_by_search_params(search_params=search_params)]

        output = StringIO()
        json.dump(obj=books, fp=output, indent=2, ensure_ascii=False)
        output.seek(0)

        return output
