from abc import ABC, abstractmethod

from fastapi import Depends

from backend import models
from backend.database import Session, get_session
from backend.db.real.authors import AuthorsDao


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


class DBFacade(DBFacadeInterface):
    """Фасад для работы с базой данных"""

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.authors_dao = AuthorsDao(session=session)

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


#  TODO в тестах подменить, что бы возвращало тестовый фасад
def get_db_facade(db_facade: DBFacade = Depends(DBFacade)) -> DBFacadeInterface:
    """Зависимость для получения фасада БД"""
    return db_facade
