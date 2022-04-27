from fastapi import HTTPException, status
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

    def get(self, book_id) -> tables.Book:
        book = (
            self.session
            .query(tables.Book)
            .filter(tables.Book.id == book_id)
            .first()
        )

        return book

    def create(self, book_data: models.BookCreate) -> tables.Book:
        """Создание книги"""
        logger.debug(f"Попытка создать новую книгу, данные: {book_data}")

        validate_errors = self._validate_book_data(book_data=book_data)
        validate_errors.update(self._validate_create_book_data(book_data=book_data))
        if validate_errors:
            logger.info(f"Книга не создана, входные данные {book_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)

        book = tables.Book(**book_data.dict())
        self.session.add(book)
        self.session.commit()

        logger.info(f"Создана новая книга: {book}")

        return book

    def delete(self, book_id) -> None:
        """Удаление книги по id"""
        book = self.get(book_id=book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        self.session.delete(book)
        self.session.commit()
        logger.info(f"Удалена книга {book}")

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



    def _validate_book_data(self, book_data: models.BookCreate) -> dict:
        errors = {}

        if book_data.issue_year <= 0:
            errors["issue_year"] = ["Год выпуска должен быть больше 0"]  # такой формат был раньше

        if book_data.page_count <= 0:
            errors["page_count"] = ["Количество страниц должно быть больше 0"]  # такой формат был раньше

        return errors

    def _validate_create_book_data(self, book_data: models.BookCreate) -> dict:
        errors = {}

        if self._get_book_by_name(book_name=book_data.name):
            errors["name"] = ["Книга с таким названием уже существует"]  # такой формат был раньше

        if self._get_book_by_isbn(book_isbn=book_data.isbn):
            errors["isbn"] = ["Книга с таким ISBN уже существует"]  # такой формат был раньше

        return errors

    def _get_book_by_name(self, book_name: str) -> tables.Book | None:
        book = (
            self.session
            .query(tables.Book)
            .filter(tables.Book.name == book_name)
            .first()
        )

        return book

    def _get_book_by_isbn(self, book_isbn: str) -> tables.Book | None:
        book = (
            self.session
                .query(tables.Book)
                .filter(tables.Book.isbn == book_isbn)
                .first()
        )

        return book
