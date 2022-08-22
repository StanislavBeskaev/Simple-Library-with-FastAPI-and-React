from loguru import logger

from backend import models, tables
from backend.exceptions import LibraryValidationException
from backend.services import BaseService
from backend.services.ws_notifications import WSConnectionManager, Notification, NotificationType


class AuthorsService(BaseService):
    """Сервис для работы с авторами"""

    def get_many(self) -> list[models.Author]:
        """Получение всех авторов"""
        logger.debug(f"AuthorsService get_many")
        return self.db_facade.get_all_authors()

    def create(self, author_data: models.AuthorCreate) -> tables.Author:
        """Создание автора"""
        logger.debug(f"Попытка создать нового автора, данные: {author_data}")

        self._validate_author_data(author_data=author_data)

        author = self.db_facade.create_author(author_data=author_data)

        logger.info(f"Создан новый автор: {author}")
        WSConnectionManager().send_notification(
            Notification(
                type=NotificationType.SUCCESS,
                text=f"Создан новый автор: {author.name} {author.surname}, {author.birth_year}"
            )
        )

        return author

    def get(self, author_id: int) -> tables.Author:
        """Получение автора по id"""
        logger.debug(f"AuthorsService запрос получения автора по id: {author_id}")
        return self.db_facade.get_author_by_id(author_id=author_id)

    def _validate_author_data(self, author_data: models.AuthorCreate) -> None:
        validate_errors = {}
        if author_data.birth_year <= 0:
            validate_errors["birth_year"] = "Год рождения должен быть больше 0"

        exist_author = self.db_facade.find_author_by_name_and_surname(
            name=author_data.name,
            surname=author_data.surname
        )

        if exist_author:
            validate_errors["name"] = "Автор с такими именем и фамилией уже существует"

        if validate_errors:
            logger.warning(f"Автор не создан, входные данные {author_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)
