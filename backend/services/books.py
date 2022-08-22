from fastapi import HTTPException
from loguru import logger

from backend import models, tables, dependencies
from backend.exceptions import LibraryValidationException
from backend.services import BaseService
from backend.services.ws_notifications import WSConnectionManager, Notification, NotificationType


class BooksService(BaseService):
    """Сервис для работы с книгами"""

    def get_many(self, search_params: dependencies.BookSearchParam) -> models.BookSearchResult:
        """Получение книг с фильтрацией"""
        logger.debug(f"Получение книг, параметры фильтрации: {search_params}")

        return models.BookSearchResult(
            count=self.db_facade.get_books_count_by_search_params(search_params=search_params),
            results=self.db_facade.get_books_by_search_params(search_params=search_params)
        )

    def get(self, book_id) -> models.Book:
        """Получение книги по id"""
        logger.debug(f"Запрос книги по id={book_id}")
        book = self.db_facade.find_book_by_id(book_id=book_id)

        if not book:
            logger.warning(f"Попытка получить информацию о не существующей книге {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        logger.debug(f"Получение информации о книге с id {book_id}")
        return book

    def create(self, book_data: models.BookCreate) -> tables.Book:
        """Создание книги"""
        logger.debug(f"Попытка создать новую книгу, данные: {book_data}")
        self._validate_create_book_data(book_data=book_data)
        book = self.db_facade.create_book(book_data=book_data)
        logger.info(f"Создана новая книга: {book}")

        WSConnectionManager().send_notification(
            Notification(type=NotificationType.SUCCESS, text=f"Создана новая книга: {book.name}")
        )

        return book

    def delete(self, book_id: int) -> None:
        """Удаление книги по id"""
        logger.debug(f"Запрос на удаление книги с id={book_id}")
        book = self.db_facade.find_book_by_id(book_id=book_id)
        if not book:
            logger.warning(f"Попытка удалить не существующую книгу {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        self.db_facade.delete_book_by_id(book_id=book_id)

        logger.info(f"Удалена книга {book}")
        WSConnectionManager().send_notification(
            Notification(type=NotificationType.ERROR, text=f"Удалена книга {book.name}")
        )

    def update(self, book_id: int, book_data: models.BookUpdate) -> tables.Book:
        """Изменение книги"""
        logger.debug(f"Попытка изменить книгу с id={book_id}, данные {book_data}")

        existing_book = self.db_facade.find_book_by_id(book_id=book_id)
        if not existing_book:
            logger.warning(f"Попытка изменить не существующую книгу {book_id}")
            raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

        self._validate_update_book_data(book_data=book_data, book_id=book_id)
        book = self.db_facade.change_book(book_id=book_id, book_data=book_data)

        logger.info(f"Изменена книга с id={book_id}, текущие параметры {book}")
        WSConnectionManager().send_notification(
            Notification(type=NotificationType.WARNING, text=f"Изменена книга {book.name}")
        )

        return book

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

        if self.db_facade.find_book_by_name(book_name=book_data.name):
            validate_errors["name"] = "Книга с таким названием уже существует"

        if self.db_facade.find_book_by_isbn(book_isbn=book_data.isbn):
            validate_errors["isbn"] = "Книга с таким ISBN уже существует"

        if validate_errors:
            logger.warning(f"Книга не создана, входные данные {book_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)

    def _validate_update_book_data(self, book_data: models.BookUpdate, book_id: int) -> None:
        validate_errors = self._get_book_data_errors(book_data=book_data)

        book_with_same_name = self.db_facade.find_book_by_name(book_name=book_data.name)
        if book_with_same_name and book_with_same_name.id != book_id:
            validate_errors["name"] = "Книга с таким названием уже существует"

        book_with_same_isbn = self.db_facade.find_book_by_isbn(book_isbn=book_data.isbn)
        if book_with_same_isbn and book_with_same_isbn.id != book_id:
            validate_errors["isbn"] = "Книга с таким ISBN уже существует"

        if validate_errors:
            logger.warning(f"Книга {book_id} не изменена, данные {book_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)
