from loguru import logger

from .. import (
    models,
    tables,
)
from ..exceptions import LibraryValidationException
from .base_service import BaseService


class BooksService(BaseService):
    """Сервис для работы с книгами"""

    # TODO параметры фильтрации
    def get_many(self) -> models.BookSearchResult:
        """Получение книг с фильтрацией"""
        # TODO формат {"count": 982, results: [{Book}, {Book}]}
        return models.BookSearchResult(
            count=self._get_books_count(),
            results=self._get_books()
        )

    # TODO параметры фильтрации
    def _get_books_count(self) -> int:
        books_count = (
            self.session
            .query(tables.Book)
            .count()
        )

        return books_count

    # TODO параметры фильтрации
    def _get_books(self) -> list[tables.Book]:
        books = (
            self.session
            .query(tables.Book)
            .order_by(tables.Book.id.desc())
            .all()
        )

        return books
