from loguru import logger
from sqlalchemy.sql.operators import desc_op

from .. import (
    models,
    tables,
)
from ..exceptions import LibraryValidationException
from .base import BaseService
from .ws_notifications import WSConnectionManager, Notification, NotificationType


class AuthorsService(BaseService):
    """Сервис для работы с авторами"""

    def get_many(self) -> list[tables.Author]:
        """Получение всех авторов"""
        authors = (
            self.session
            .query(tables.Author)
            .order_by(desc_op(tables.Author.id))
            .all()
        )

        return authors

    def create(self, author_data: models.AuthorCreate) -> tables.Author:
        """Создание автора"""
        logger.debug(f"Попытка создать нового автора, данные: {author_data}")

        self._validate_author_data(author_data=author_data)

        author = tables.Author(**author_data.dict())
        self.session.add(author)
        self.session.commit()

        logger.info(f"Создан новый автор: {author}")
        WSConnectionManager().send_notification(
            Notification(
                type=NotificationType.SUCCESS,
                text=f"Создан новый автор: {author.name} {author.surname}, {author.birth_year}"
            )
        )

        return author

    def get(self, author_id) -> tables.Author:
        author = (
            self.session
            .query(tables.Author)
            .filter(tables.Author.id == author_id)
            .first()
        )

        return author

    def _validate_author_data(self, author_data: models.AuthorCreate) -> None:
        validate_errors = {}
        if author_data.birth_year <= 0:
            validate_errors["birth_year"] = "Год рождения должен быть больше 0"

        exist_author = (
            self.session
            .query(tables.Author)
            .filter(
                tables.Author.name == author_data.name,
                tables.Author.surname == author_data.surname
            )
            .first()
        )

        if exist_author:
            validate_errors["name"] = "Автор с такими именем и фамилией уже существует"

        if validate_errors:
            logger.warning(f"Автор не создан, входные данные {author_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)
