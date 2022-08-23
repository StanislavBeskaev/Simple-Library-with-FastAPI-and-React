from loguru import logger

from backend import models
from backend.db.facade import DBFacadeInterface
from backend.db.mock.authors import MockAuthorsDao
from backend.db.mock.books import MockBooksDao
from backend.dependencies import BookSearchParam


def mock_get_db_facade() -> DBFacadeInterface:
    logger.debug("call mock_get_db_facade")
    return MockDBFacade()


class MockDBFacade(DBFacadeInterface):
    """Mock фасада базы данных для тестов"""

    def __init__(self):
        self.mock_authors_dao = MockAuthorsDao()
        self.mock_books_dao = MockBooksDao()

    def get_all_authors(self) -> list[models.Author]:
        return self.mock_authors_dao.get_all_authors()

    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        return self.mock_authors_dao.create_author(author_data=author_data)

    def get_author_by_id(self, author_id: int) -> models.Author:
        return self.mock_authors_dao.get_author_by_id(author_id=author_id)

    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        return self.mock_authors_dao.find_author_by_name_and_surname(name=name, surname=surname)

    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        return self.mock_books_dao.get_books_by_search_params(search_params=search_params)

    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        return self.mock_books_dao.get_books_count_by_search_params(search_params=search_params)

    def find_book_by_id(self, book_id: int) -> models.Book | None:
        return self.mock_books_dao.find_book_by_id(book_id=book_id)

    def create_book(self, book_data: models.BookCreate) -> models.Book:
        return self.mock_books_dao.create_book(book_data=book_data)

    def delete_book_by_id(self, book_id: int) -> None:
        self.mock_books_dao.delete_book_by_id(book_id=book_id)

    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        return self.mock_books_dao.change_book(book_id=book_id, book_data=book_data)

    def find_book_by_name(self, book_name: str) -> models.Book | None:
        return self.mock_books_dao.find_book_by_name(book_name=book_name)

    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        return self.mock_books_dao.find_book_by_isbn(book_isbn=book_isbn)
