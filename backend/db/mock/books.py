from copy import deepcopy

from loguru import logger

from backend import models, tables
from backend.db.dao.books import BooksDaoInterface
from backend.decorators import model_result
from backend.dependencies import BookSearchParam


class MockBooksDao(BooksDaoInterface):
    """Mock класс для работы с книгами в БД"""
    test_authors = [
        tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),
        tables.Author(id=2, name="Автор", surname="Второй", birth_year=2),
        tables.Author(id=3, name="Автор", surname="Третий", birth_year=3),
    ]

    test_books = [
        tables.Book(id=1, name="рассказ 1", author=1, isbn="tale-isbn-1", issue_year=1203, page_count=12),
        tables.Book(id=2, name="рассказ 2", author=1, isbn="tale-isbn-2", issue_year=1590, page_count=14),
        tables.Book(id=3, name="рассказ 3", author=1, isbn="tale-isbn-3", issue_year=768, page_count=19),
        tables.Book(id=4, name="рассказ 4", author=1, isbn="tale-isbn-4", issue_year=1867, page_count=17),
        tables.Book(id=5, name="рассказ 5", author=1, isbn="tale-isbn-5", issue_year=1917, page_count=9),
        tables.Book(id=6, name="история 1", author=2, isbn="history-isbn-1", issue_year=1241, page_count=20),
        tables.Book(id=7, name="история 2", author=2, isbn="history-isbn-2", issue_year=1, page_count=39),
        tables.Book(id=8, name="история 3", author=2, isbn="history-isbn-3", issue_year=1913, page_count=33),
        tables.Book(id=9, name="история 4", author=2, isbn="history-isbn-4", issue_year=1171, page_count=27),
        tables.Book(id=10, name="история 5", author=2, isbn="history-isbn-5", issue_year=1764, page_count=29),
        tables.Book(id=11, name="роман 1", author=3, isbn="novel-isbn-1", issue_year=1712, page_count=40),
        tables.Book(id=12, name="роман 2", author=3, isbn="novel-isbn-2", issue_year=1812, page_count=112),
        tables.Book(id=13, name="роман 3", author=3, isbn="novel-isbn-3", issue_year=1912, page_count=150),
        tables.Book(id=14, name="роман 4", author=3, isbn="novel-isbn-4", issue_year=2012, page_count=78),
        tables.Book(id=15, name="роман 5", author=3, isbn="novel-isbn-5", issue_year=1692, page_count=201),
    ]

    @model_result(models.Book)
    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        result = self._get_books_by_search_params(search_params=search_params)

        start = (search_params.page - 1) * search_params.page_size
        end = start + search_params.page_size
        logger.debug(f"get_books_by_search_params {start=} {end=}")

        result = result[start:end]
        return result

    def _get_books_by_search_params(self, search_params: BookSearchParam) -> list[tables.Book]:
        result = sorted(self.test_books, key=lambda book: book.id, reverse=True)

        if search_params.name:
            result = [book for book in result if search_params.name.lower() in book.name.lower()]

        if search_params.issue_year_gte:
            result = [book for book in result if book.issue_year >= search_params.issue_year_gte]

        if search_params.issue_year_lte:
            result = [book for book in result if book.issue_year <= search_params.issue_year_lte]

        if search_params.page_count_gte:
            result = [book for book in result if book.page_count >= search_params.page_count_gte]

        if search_params.page_count_lte:
            result = [book for book in result if book.page_count <= search_params.page_count_lte]

        if search_params.author:
            result = [book for book in result if book.author == search_params.author]

        return result

    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        return len(self._get_books_by_search_params(search_params=search_params))

    @model_result(models.Book)
    def find_book_by_id(self, book_id: int) -> models.Book | None:
        return self._find_book_by_id(book_id=book_id)

    def _find_book_by_id(self, book_id: int) -> models.Book | None:
        candidate = next(
            (book for book in self.test_books if book.id == book_id),
            None
        )

        return candidate

    @model_result(models.Book)
    def create_book(self, book_data: models.BookCreate) -> models.Book:
        db_book = tables.Book(**book_data.dict(), id=len(self.test_books) + 1)
        return db_book

    def delete_book_by_id(self, book_id: int) -> None:
        pass

    @model_result(models.Book)
    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        db_book = deepcopy(self._find_book_by_id(book_id=book_id))
        for attr, value in vars(book_data).items():
            setattr(db_book, attr, value)
        return db_book

    @model_result(models.Book)
    def find_book_by_name(self, book_name: str) -> models.Book | None:
        candidate = next(
            (book for book in self.test_books if book.name == book_name),
            None
        )

        return candidate

    @model_result(models.Book)
    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        candidate = next(
            (book for book in self.test_books if book.isbn == book_isbn),
            None
        )

        return candidate
