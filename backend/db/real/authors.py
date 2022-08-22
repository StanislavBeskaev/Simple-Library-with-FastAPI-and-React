from fastapi import HTTPException
from sqlalchemy.sql.operators import desc_op

from loguru import logger

from backend import models, tables
from backend.decorators import model_result
from backend.db.real.base import BaseDAO


class AuthorsDao(BaseDAO):
    """Класс для работы с авторами в БД"""

    @model_result(models.Author)
    def get_all_authors(self) -> list[models.Author]:
        """Получение всех авторов"""
        logger.debug(f"AuthorsDao get_all_authors")
        db_authors = (
            self.session
            .query(tables.Author)
            .order_by(desc_op(tables.Author.id))
            .all()
        )

        return db_authors

    @model_result(models.Author)
    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        """Создание автора в БД"""
        logger.debug(f"AuthorsDao create_author, {author_data=}")
        db_author = tables.Author(**author_data.dict())
        self.session.add(db_author)
        self.session.commit()

        return db_author

    @model_result(models.Author)
    def get_author_by_id(self, author_id: int) -> models.Author:
        """Получение автора по id"""
        db_author = (
            self.session
                .query(tables.Author)
                .filter(tables.Author.id == author_id)
                .first()
        )

        # TODO подумать, может кидать DB исключение?
        if not db_author:
            raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")

        return db_author

    @model_result(models.Author)
    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        """Поиск автора по имени и фамилии"""
        candidate = (
            self.session
            .query(tables.Author)
            .filter(
                    tables.Author.name == name,
                    tables.Author.surname == surname
                )
            .first()
        )

        return candidate
