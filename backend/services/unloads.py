import json
from io import StringIO

from loguru import logger

from backend import dependencies
from backend.services import BaseService


class UnloadService(BaseService):
    """Сервис для выгрузки данных в json"""

    def get_authors(self) -> StringIO:
        """Получение выгрузки всех авторов"""
        logger.debug(f"Запрошена выгрузка авторов")
        authors = [author.dict() for author in self.db_facade.get_all_authors()]

        output = StringIO()
        json.dump(obj=authors, fp=output, indent=2, ensure_ascii=False)
        output.seek(0)

        return output

    def get_books(self, search_params: dependencies.BookSearchParam):
        """Получение выгрузки книг по переданным параметрам"""
        logger.debug(f"Запрошена выгрузка книг по параметрам: {search_params}")
        books = [book.dict() for book in self.db_facade.get_books_by_search_params(search_params=search_params)]

        output = StringIO()
        json.dump(obj=books, fp=output, indent=2, ensure_ascii=False)
        output.seek(0)

        return output
