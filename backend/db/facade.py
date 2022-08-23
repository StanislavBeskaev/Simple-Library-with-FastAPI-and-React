from abc import ABC, abstractmethod

from fastapi import Depends

from backend import models
from backend.database import Session, get_session
from backend.db.dao.authors import AuthorsDao
from backend.db.dao.books import BooksDao
from backend.dependencies import BookSearchParam


class DBFacadeInterface(ABC):
    """Интерфейс фасада базы данных"""

    @abstractmethod
    def get_all_authors(self) -> list[models.Author]:
        ...

    @abstractmethod
    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        ...

    @abstractmethod
    def get_author_by_id(self, author_id: int) -> models.Author:
        ...

    @abstractmethod
    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        ...

    @abstractmethod
    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        ...

    @abstractmethod
    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        ...

    @abstractmethod
    def find_book_by_id(self, book_id: int) -> models.Book | None:
        ...

    @abstractmethod
    def create_book(self, book_data: models.BookCreate) -> models.Book:
        ...

    @abstractmethod
    def delete_book_by_id(self, book_id: int) -> None:
        ...

    @abstractmethod
    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        ...

    @abstractmethod
    def find_book_by_name(self, book_name: str) -> models.Book | None:
        ...

    @abstractmethod
    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        ...


class DBFacade(DBFacadeInterface):
    """Фасад для работы с базой данных"""

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.authors_dao = AuthorsDao(session=session)
        self.books_dao = BooksDao(session=session)

    def get_all_authors(self) -> list[models.Author]:
        """Получение всех авторов"""
        return self.authors_dao.get_all_authors()

    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        """Создание автора в БД"""
        return self.authors_dao.create_author(author_data=author_data)

    def get_author_by_id(self, author_id: int) -> models.Author:
        """Получение автора по id"""
        return self.authors_dao.get_author_by_id(author_id=author_id)

    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        """Поиск автора по имени и фамилии"""
        return self.authors_dao.find_author_by_name_and_surname(name=name, surname=surname)

    def get_books_by_search_params(self, search_params: BookSearchParam) -> list[models.Book]:
        """Получение книг по поисковым параметрам"""
        return self.books_dao.get_books_by_search_params(search_params=search_params)

    def get_books_count_by_search_params(self, search_params: BookSearchParam) -> int:
        """Получение количества книг удовлетворяющих поисковым параметрам"""
        return self.books_dao.get_books_count_by_search_params(search_params=search_params)

    def find_book_by_id(self, book_id: int) -> models.Book | None:
        """Поиск книги по id"""
        return self.books_dao.find_book_by_id(book_id=book_id)

    def create_book(self, book_data: models.BookCreate) -> models.Book:
        """Создание книги"""
        return self.books_dao.create_book(book_data=book_data)

    def delete_book_by_id(self, book_id: int) -> None:
        """Удаление книги по id"""
        self.books_dao.delete_book_by_id(book_id=book_id)

    def change_book(self, book_id: int, book_data: models.BookUpdate) -> models.Book:
        """Изменение книги"""
        return self.books_dao.change_book(book_id=book_id, book_data=book_data)

    def find_book_by_name(self, book_name: str) -> models.Book | None:
        """Поиск книги по имени"""
        return self.books_dao.find_book_by_name(book_name=book_name)

    def find_book_by_isbn(self, book_isbn: str) -> models.Book | None:
        """Поиск книги по ISBN"""
        return self.books_dao.find_book_by_isbn(book_isbn=book_isbn)


def get_db_facade(db_facade: DBFacade = Depends(DBFacade)) -> DBFacadeInterface:
    """Зависимость для получения фасада БД"""
    return db_facade
