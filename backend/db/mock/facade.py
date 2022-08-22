from loguru import logger

from backend import models
from backend.db.facade import DBFacadeInterface
from backend.db.mock.authors import MockAuthorsDao
from backend.dependencies import BookSearchParam


def mock_get_db_facade() -> DBFacadeInterface:
    logger.debug("call mock_get_db_facade")
    return MockDBFacade()


class MockDBFacade(DBFacadeInterface):
    """Mock фасада базы данных для тестов"""
    def __init__(self):
        self.mock_authors_dao = MockAuthorsDao()

    def get_all_authors(self) -> list[models.Author]:
        return self.mock_authors_dao.get_all_authors()

    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        return self.mock_authors_dao.create_author(author_data=author_data)

    def get_author_by_id(self, author_id: int) -> models.Author:
        return self.mock_authors_dao.get_author_by_id(author_id=author_id)

    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        return self.mock_authors_dao.find_author_by_name_and_surname(name=name, surname=surname)

    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        ...

    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        ...

    def find_book_by_id(self, book_id: int) -> models.Book | None:
        ...

    def create_book(self, book_data: models.BookCreate) -> models.Book:
        ...

    def delete_book_by_id(self, book_id: int) -> None:
        ...

    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        ...

    def find_book_by_name(self, book_name: str) -> models.Book | None:
        ...

    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        ...
