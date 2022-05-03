from .. import models
from .. import tables
from .base import BaseTestCase, override_get_session


test_authors = [
    tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),
    tables.Author(id=2, name="Автор", surname="Второй", birth_year=2),
    tables.Author(id=3, name="Автор", surname="Третий", birth_year=3),
]


class TestAuthors(BaseTestCase):
    authors_url = "/api_library/authors/"

    def setUp(self) -> None:
        test_session = next(override_get_session())
        test_session.bulk_save_objects(test_authors)
        test_session.commit()

    def tearDown(self) -> None:
        test_session = next(override_get_session())
        test_session.query(tables.Author).delete()
        test_session.commit()

    def test_get_authors(self):
        response = self.client.get(self.authors_url)

        self.assertEqual(response.status_code, 200)
        expected_authors = [models.Author.from_orm(author).dict() for author in self.with_id_sort(test_authors)]
        self.assertEqual(expected_authors, response.json())

    def test_get_author_success(self):
        response = self.client.get(f"{self.authors_url}1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), models.Author.from_orm(test_authors[0]).dict())

    def test_get_author_not_found(self):
        response = self.client.get(f"{self.authors_url}4")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Author with id 4 not found"})

    def test_create_author_success(self):
        response = self.client.post(
            self.authors_url,
            json={
                "name": "Автор",
                "surname": "Четвёртый",
                "birth_year": 4
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "name": "Автор",
                "surname": "Четвёртый",
                "birth_year": 4,
                "id": 4
            }
        )

    def test_create_author_failed(self):
        response = self.client.post(
            self.authors_url,
            json={
                "name": "Автор",
                "surname": "Первый",
                "birth_year": 0
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'birth_year': 'Год рождения должен быть больше 0',
                'name': 'Автор с такими именем и фамилией уже существует'
            }
        )
