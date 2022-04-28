from loguru import logger
from sqlalchemy.sql.operators import desc_op

from .. import (
    models,
    tables,
)
from ..exceptions import LibraryValidationException
from .base_service import BaseService


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

        validate_errors = self._validate_author_data(author_data=author_data)
        if validate_errors:
            logger.warning(f"Автор не создан, входные данные {author_data}; ошибки валидации: {validate_errors}")
            raise LibraryValidationException(errors=validate_errors)

        author = tables.Author(**author_data.dict())
        self.session.add(author)
        self.session.commit()
        logger.info(f"Создан новый автор: {author}")

        return author

    def get(self, author_id) -> tables.Author:
        author = (
            self.session
            .query(tables.Author)
            .filter(tables.Author.id == author_id)
            .first()
        )

        return author

    def _validate_author_data(self, author_data: models.AuthorCreate) -> dict:
        errors = {}
        if author_data.birth_year <= 0:
            errors["birth_year"] = ["Год рождения должен быть больше 0"]  # такой формат был раньше

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
            errors["name"] = ["Автор с такими именем и фамилией уже существует"]  # такой формат был раньше

        return errors
