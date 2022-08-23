from typing import Any
from unittest import TestCase

from fastapi.testclient import TestClient

from backend import models
from backend.db.facade import get_db_facade
from backend.db.mock.facade import mock_get_db_facade
from backend.main import app


class BaseLibraryTestCase(TestCase):
    """Базовый класс для тестов библиотеки"""
    client = TestClient(app)

    @classmethod
    def setUpClass(cls) -> None:
        app.dependency_overrides[get_db_facade] = mock_get_db_facade

    @classmethod
    def tearDownClass(cls) -> None:
        app.dependency_overrides = {}

    @staticmethod
    def with_id_sort(elements: list[Any]) -> list[Any]:
        return sorted(elements, key=lambda element: element.id, reverse=True)

    def convert_to_dicts(self, items: list, model=models.Book) -> list[dict]:
        return [model.from_orm(book).dict() for book in self.with_id_sort(items)]
