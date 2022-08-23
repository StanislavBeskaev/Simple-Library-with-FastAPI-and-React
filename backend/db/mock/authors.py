from fastapi import HTTPException

from backend import models, tables
from backend.decorators import model_result
from backend.db.dao.authors import AuthorsDaoInterface


class MockAuthorsDao(AuthorsDaoInterface):
    """Mock класс для работы с авторами в БД"""
    test_authors = [
        tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),
        tables.Author(id=2, name="Автор", surname="Второй", birth_year=2),
        tables.Author(id=3, name="Автор", surname="Третий", birth_year=3),
    ]

    @model_result(models.Author)
    def get_all_authors(self) -> list[models.Author]:
        return sorted(self.test_authors, key=lambda item: item.id, reverse=True)

    @model_result(models.Author)
    def create_author(self, author_data: models.AuthorCreate) -> models.Author:
        mock_author = tables.Author(**author_data.dict(), id=4)
        # TODO проверить ли добавление автора в список?
        return mock_author

    @model_result(models.Author)
    def get_author_by_id(self, author_id: int) -> models.Author:
        mock_author = next((author for author in self.test_authors if author.id == author_id), None)
        if not mock_author:
            raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")

        return mock_author

    @model_result(models.Author)
    def find_author_by_name_and_surname(self, name: str, surname: str) -> models.Author | None:
        mock_author = next(
            (author for author in self.test_authors if author.name == name and author.surname == surname),
            None
        )
        return mock_author
