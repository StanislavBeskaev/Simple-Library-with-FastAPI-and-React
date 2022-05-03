from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm import Query
from sqlalchemy.sql.operators import ilike_op, desc_op

from .. import models, tables, dependencies
from ..exceptions import LibraryValidationException
from .base import BaseService
from .ws_notifications import WSConnectionManager, Notification, NotificationType


class BooksService(BaseService):
    """Сервис для работы с книгами"""

    def get_many(self, search_params: dependencies.BookSearchParam) -> models.BookSearchResult:
        """Получение книг с фильтрацией"""
        logger.debug(f"Получение книг, параметры фильтрации: {search_params}")

        return models.BookSearchResult(
            count=self._get_books_count(search_params=search_params),
            results=self.get_books_by_search_params(search_params=search_params)
        )

    def get_books_by_search_params(self, search_params: dependencies.BookSearchParam) -> list[tables.Book]:
        books = (
            self._get_search_books_query(search_params=search_params)
            .order_by(desc_op(tables.Book.id))
            .offset((search_params.page - 1) * search_params.page_size)
            .limit(search_params.page_size)
            .all()
        )

        return books

    def get(self, book_id) -> tables.Book:
        book = self._get_book_by_id(book_id=book_id)

        if not book:
            logger.warning(f"Попытка получить информацию о не существующей книге {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        return book

    def create(self, book_data: models.BookCreate) -> tables.Book:
        """Создание книги"""
        logger.debug(f"Попытка создать новую книгу, данные: {book_data}")

        self._validate_create_book_data(book_data=book_data)

        book = tables.Book(**book_data.dict())
        self.session.add(book)
        self.session.commit()

        logger.info(f"Создана новая книга: {book}")

        WSConnectionManager().send_notification(
            Notification(type=NotificationType.SUCCESS, text=f"Создана новая книга: {book.name}")
        )

        return book

    def delete(self, book_id) -> None:
        """Удаление книги по id"""
        book = self._get_book_by_id(book_id=book_id)
        if not book:
            logger.warning(f"Попытка удалить не существующую книгу {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        self.session.delete(book)
        self.session.commit()

        logger.info(f"Удалена книга {book}")
        WSConnectionManager().send_notification(
            Notification(type=NotificationType.ERROR, text=f"Удалена книга {book.name}")
        )

    def update(self, book_id: int, book_data: models.BookUpdate) -> tables.Book:
        """Изменение книги"""
        logger.debug(f"Попытка изменить книгу {book_id}, данные {book_data}")

        book = self._get_book_by_id(book_id=book_id)
        if not book:
            logger.warning(f"Попытка изменить не существующую книгу {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        self._validate_update_book_data(book_data=book_data, book_id=book_id)

        for attr, value in vars(book_data).items():
            setattr(book, attr, value)

        self.session.add(book)
        self.session.commit()

        logger.info(f"Изменена книга {book}, текущие параметры {book}")
        WSConnectionManager().send_notification(
            Notification(type=NotificationType.WARNING, text=f"Изменена книга {book.name}")
        )

        return book

    def _get_book_by_id(self, book_id) -> tables.Book:
        book = (
            self.session
            .query(tables.Book)
            .filter(tables.Book.id == book_id)
            .first()
        )

        return book

    def _get_books_count(self, search_params: dependencies.BookSearchParam) -> int:
        books_count = self._get_search_books_query(search_params=search_params).count()

        return books_count

    def _get_search_books_query(self, search_params: dependencies.BookSearchParam) -> Query:
        book_query = self.session.query(tables.Book)

        if search_params.name:
            book_query = book_query.filter(ilike_op(tables.Book.name, f"%{search_params.name.lower()}%"))

        if search_params.issue_year_gte:
            book_query = book_query.filter(tables.Book.issue_year >= search_params.issue_year_gte)

        if search_params.issue_year_lte:
            book_query = book_query.filter(tables.Book.issue_year <= search_params.issue_year_lte)

        if search_params.page_count_gte:
            book_query = book_query.filter(tables.Book.page_count >= search_params.page_count_gte)

        if search_params.page_count_lte:
            book_query = book_query.filter(tables.Book.page_count <= search_params.page_count_lte)

        if search_params.author:
            book_query = book_query.filter(tables.Book.author == search_params.author)

        return book_query

    @staticmethod
    def _get_book_data_errors(book_data: models.BookCreate | models.BookUpdate) -> dict:
        errors = {}

        if book_data.issue_year <= 0:
            errors["issue_year"] = "Год выпуска должен быть больше 0"

        if book_data.page_count <= 0:
            errors["page_count"] = "Количество страниц должно быть больше 0"

        return errors

    def _validate_create_book_data(self, book_data: models.BookCreate) -> None:
        validate_errors = self._get_book_data_errors(book_data=book_data)

        if self._get_book_by_name(book_name=book_data.name):
            validate_errors["name"] = "Книга с таким названием уже существует"

        if self._get_book_by_isbn(book_isbn=book_data.isbn):
            validate_errors["isbn"] = "Книга с таким ISBN уже существует"

        if validate_errors:
            logger.warning(f"Книга не создана, входные данные {book_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)

    def _validate_update_book_data(self, book_data: models.BookUpdate, book_id: int) -> None:
        validate_errors = self._get_book_data_errors(book_data=book_data)

        book_with_same_name = self._get_book_by_name(book_name=book_data.name)
        if book_with_same_name and book_with_same_name.id != book_id:
            validate_errors["name"] = "Книга с таким названием уже существует"

        book_with_same_isbn = self._get_book_by_isbn(book_isbn=book_data.isbn)
        if book_with_same_isbn and book_with_same_isbn.id != book_id:
            validate_errors["isbn"] = "Книга с таким ISBN уже существует"

        if validate_errors:
            logger.warning(f"Книга {book_id} не изменена, данные {book_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)

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
