from typing import (
    List,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from loguru import logger
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class AuthorsService:
    """Сервис для работы с авторами"""

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self):
        """Получение всех авторов"""
        authors = (
            self.session
            .query(tables.Author)
            .order_by(tables.Author.id.desc())
            .all()
        )

        return authors

    def create(self, author_data: models.AuthorCreate) -> tables.Author:
        """Создание автора"""
        logger.debug(f"Попытка создать нового автора, данные: {author_data}")
        author = tables.Author(**author_data.dict())
        self.session.add(author)
        self.session.commit()
        logger.info(f"Создан новый автор: {author}")

        # TODO логи
        # TODO реализовать проверки
        # errors = {}
        # if Author.objects.filter(name=data['name'], surname=data['surname']).exists():
        #     errors["name"] = "Автор с такими именем и фамилией уже существует"
        #
        # if data['birth_year'] <= 0:
        #     errors["birth_year"] = "Год рождения должен быть больше 0"
        # if errors:
        #     raise serializers.ValidationError(errors)
        # return data

        return author
