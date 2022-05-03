from pydantic import parse_obj_as

from .. import models
from .. import tables
from .base import BaseTestCase, override_get_session


test_authors = [
    tables.Author(id=3, name="Автор", surname="Третий", birth_year=3),
    tables.Author(id=2, name="Автор", surname="Второй", birth_year=2),
    tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),
]


class TestAuthors(BaseTestCase):

    def setUp(self) -> None:
        test_session = next(override_get_session())
        test_session.bulk_save_objects(test_authors)
        test_session.commit()

    def tearDown(self) -> None:
        test_session = next(override_get_session())
        test_session.query(tables.Author).delete()
        test_session.commit()

    def test_get_authors(self):
        response = self.client.get("/api_library/authors/")

        self.assertEqual(response.status_code, 200)
        expected_authors = [models.Author.from_orm(author) for author in test_authors]
        response_authors = parse_obj_as(list[models.Author], obj=response.json())
        self.assertEqual(expected_authors, response_authors)

    def test_get_author_success(self):
        response = self.client.get("/api_library/authors/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), models.Author.from_orm(test_authors[2]).dict())

    def test_get_author_not_found(self):
        response = self.client.get("/api_library/authors/4")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Author with id 4 not found"})
