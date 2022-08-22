from sqlalchemy.orm import Query
from sqlalchemy.sql.operators import ilike_op, desc_op

from backend import models, tables
from backend.db.real.base import BaseDAO
from backend.dependencies import BookSearchParam


class BooksDao(BaseDAO):
    """Класс для работы с книгами в БД"""

    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        """Получение книг удовлетворяющих поисковым параметрам"""
        db_books = (
            self._get_search_books_query(search_params=search_params)
            .order_by(desc_op(tables.Book.id))
            .offset((search_params.page - 1) * search_params.page_size)
            .limit(search_params.page_size)
            .all()
        )

        books = [models.Book.from_orm(db_book) for db_book in db_books]
        return books

    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        """Получение количества книг удовлетворяющих поисковым параметрам"""
        books_count = self._get_search_books_query(search_params=search_params).count()

        return books_count

    def _get_search_books_query(self, search_params: BookSearchParam) -> Query:
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

    def find_book_by_id(self, book_id: int) -> models.Book | None:
        """Поиск книги по id"""
        candidate = self._find_book_by_id(book_id=book_id)

        if not candidate:
            return None

        return models.Book.from_orm(candidate)

    def _find_book_by_id(self, book_id: int) -> tables.Book | None:
        return (
            self.session
            .query(tables.Book)
            .filter(tables.Book.id == book_id)
            .first()
        )

    def create_book(self, book_data: models.BookCreate) -> models.Book:
        """Создание книги"""
        db_book = tables.Book(**book_data.dict())
        self.session.add(db_book)
        self.session.commit()

        return models.Book.from_orm(db_book)

    def delete_book_by_id(self, book_id: int) -> None:
        """Удаление книги по id"""
        db_book = self._find_book_by_id(book_id=book_id)

        self.session.delete(db_book)
        self.session.commit()

    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        """Изменение книги"""
        db_book = self._find_book_by_id(book_id=book_id)
        for attr, value in vars(book_data).items():
            setattr(db_book, attr, value)

        self.session.add(db_book)
        self.session.commit()

        return models.Book.from_orm(db_book)

    def find_book_by_name(self, book_name: str) -> models.Book | None:
        """Поиск книги по имени"""
        candidate = (
            self.session
            .query(tables.Book)
            .filter(tables.Book.name == book_name)
            .first()
        )
        if not candidate:
            return None

        return models.Book.from_orm(candidate)

    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        """Поиск книги по ISBN"""
        candidate = (
            self.session
            .query(tables.Book)
            .filter(tables.Book.isbn == book_isbn)
            .first()
        )
        if not candidate:
            return None

        return models.Book.from_orm(candidate)
