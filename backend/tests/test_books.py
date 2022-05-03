from .. import models
from .. import tables
from .base import BaseTestCase, override_get_session

test_authors = [
    tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),
    tables.Author(id=2, name="Автор", surname="Второй", birth_year=2),
    tables.Author(id=3, name="Автор", surname="Третий", birth_year=3),
]

test_books = [
    tables.Book(id=1, name="рассказ 1", author=1, isbn="tale-isbn-1", issue_year=1203, page_count=12),
    tables.Book(id=2, name="рассказ 2", author=1, isbn="tale-isbn-2", issue_year=1590, page_count=14),
    tables.Book(id=3, name="рассказ 3", author=1, isbn="tale-isbn-3", issue_year=768, page_count=19),
    tables.Book(id=4, name="рассказ 4", author=1, isbn="tale-isbn-4", issue_year=1867, page_count=17),
    tables.Book(id=5, name="рассказ 5", author=1, isbn="tale-isbn-5", issue_year=1917, page_count=9),
    tables.Book(id=6, name="история 1", author=2, isbn="history-isbn-1", issue_year=1241, page_count=20),
    tables.Book(id=7, name="история 2", author=2, isbn="history-isbn-2", issue_year=1, page_count=39),
    tables.Book(id=8, name="история 3", author=2, isbn="history-isbn-3", issue_year=1913, page_count=33),
    tables.Book(id=9, name="история 4", author=2, isbn="history-isbn-4", issue_year=1171, page_count=27),
    tables.Book(id=10, name="история 5", author=2, isbn="history-isbn-5", issue_year=1764, page_count=29),
    tables.Book(id=11, name="роман 1", author=3, isbn="novel-isbn-1", issue_year=1712, page_count=40),
    tables.Book(id=12, name="роман 2", author=3, isbn="novel-isbn-2", issue_year=1812, page_count=112),
    tables.Book(id=13, name="роман 3", author=3, isbn="novel-isbn-3", issue_year=1912, page_count=150),
    tables.Book(id=14, name="роман 4", author=3, isbn="novel-isbn-4", issue_year=2012, page_count=78),
    tables.Book(id=15, name="роман 5", author=3, isbn="novel-isbn-5", issue_year=1692, page_count=201),
]


class BaseTestBooks(BaseTestCase):
    books_url = "/api_library/books/"

    def setUp(self) -> None:
        test_session = next(override_get_session())
        test_session.bulk_save_objects(test_authors)
        test_session.bulk_save_objects(test_books)
        test_session.commit()

    def tearDown(self) -> None:
        test_session = next(override_get_session())
        test_session.query(tables.Author).delete()
        test_session.query(tables.Book).delete()
        test_session.commit()


class TestFindBooks(BaseTestBooks):
    def test_find_books_pagination(self):
        response = self.client.get(self.books_url, params={"page_size": 5, "page": 2})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books)
        self._check_books_search_result(
            response=response,
            searched_books=self._convert_to_dicts(books=test_books),
            results_books=searched_books[5:10]
        )

        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books)
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"page_size": 10})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books)
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books[:10]
        )

    def _convert_to_dicts(self, books: list[tables.Book]) -> list[dict]:
        return [models.Book.from_orm(book).dict() for book in self.with_id_sort(books)]

    def _check_books_search_result(self, response, searched_books: list[dict], results_books: list[dict]):
        expected_books_result = models.BookSearchResult(
            count=len(searched_books),
            results=results_books
        )
        self.assertEqual(response.json(), expected_books_result.dict())

    def test_find_books_by_name(self):
        response = self.client.get(self.books_url, params={"name": "рассказ"})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[:5])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books

        )

        response = self.client.get(self.books_url, params={"name": "история"})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[5:10])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"name": "роман"})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[10:])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"name": 3})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[2::5])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

    def test_find_books_by_year(self):
        response = self.client.get(self.books_url, params={"issue_year__gte": 1700, "issue_year__lte": 1800})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[
            book for book in test_books if 1700 <= book.issue_year <= 1800
        ])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"issue_year__gte": 1590})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[book for book in test_books if 1590 <= book.issue_year])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"issue_year__lte": 1241})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[book for book in test_books if book.issue_year <= 1241])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

    def test_find_books_by_page_count(self):
        response = self.client.get(self.books_url, params={"page_count__gte": 17, "page_count__lte": 78})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[
            book for book in test_books if 17 <= book.page_count <= 79
        ])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"page_count__gte": 29})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[
            book for book in test_books if 29 <= book.page_count
        ])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

        response = self.client.get(self.books_url, params={"page_count__lte": 27})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=[
            book for book in test_books if book.page_count <= 27
        ])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books
        )

    def test_find_books_by_author(self):
        response = self.client.get(self.books_url, params={"author": 1})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[:5])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books

        )

        response = self.client.get(self.books_url, params={"author": 2})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[5:10])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books

        )

        response = self.client.get(self.books_url, params={"author": 3})
        self.assertEqual(response.status_code, 200)
        searched_books = self._convert_to_dicts(books=test_books[10:])
        self._check_books_search_result(
            response=response,
            searched_books=searched_books,
            results_books=searched_books

        )


class TestBookCRUD(BaseTestBooks):

    def test_get_book_success(self):
        response = self.client.get(f"{self.books_url}1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            models.Book.from_orm(test_books[0]).dict()
        )

        response = self.client.get(f"{self.books_url}7")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            models.Book.from_orm(test_books[6]).dict()
        )

        response = self.client.get(f"{self.books_url}13")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            models.Book.from_orm(test_books[12]).dict()
        )

    def test_get_book_not_found(self):
        response = self.client.get(f"{self.books_url}16")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 16 not found"})

        response = self.client.get(f"{self.books_url}125")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 125 not found"})

        response = self.client.get(f"{self.books_url}100000")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 100000 not found"})

    def test_create_book_success(self):
        response = self.client.post(
            self.books_url,
            json={
                "name": "Новая книга",
                "author": 1,
                "isbn": "new-isbn",
                "issue_year": 1991,
                "page_count": 30
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "name": "Новая книга",
                "author": 1,
                "isbn": "new-isbn",
                "issue_year": 1991,
                "page_count": 30,
                "id": 16
            }
        )

    def test_create_book_failed(self):
        response = self.client.post(
            self.books_url,
            json={
                "name": "рассказ 1",
                "author": 1,
                "isbn": "tale-isbn-2",
                "issue_year": -2,
                "page_count": 0
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует',
                'isbn': 'Книга с таким ISBN уже существует',
                'issue_year': 'Год выпуска должен быть больше 0',
                'page_count': 'Количество страниц должно быть больше 0'
            }
        )

        response = self.client.post(
            self.books_url,
            json={
                "name": "рассказ 1",
                "author": 1,
                "isbn": "tale-isbn-2",
                "issue_year": 12,
                "page_count": 0
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует',
                'isbn': 'Книга с таким ISBN уже существует',
                'page_count': 'Количество страниц должно быть больше 0'
            }
        )

        response = self.client.post(
            self.books_url,
            json={
                "name": "рассказ 1",
                "author": 1,
                "isbn": "tale-isbn-2",
                "issue_year": 12,
                "page_count": 14
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует',
                'isbn': 'Книга с таким ISBN уже существует'
            }
        )

        response = self.client.post(
            self.books_url,
            json={
                "name": "рассказ 1",
                "author": 1,
                "isbn": "tale-isbn-6",
                "issue_year": 12,
                "page_count": 14
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует'
            }
        )
