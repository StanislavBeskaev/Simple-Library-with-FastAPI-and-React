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


class TestBooks(BaseTestCase):
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
        searched_books = self._convert_to_dicts(books=test_books[10:15])
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
        searched_books = self._convert_to_dicts(books=[book for book in test_books if book.issue_year >= 1590])
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
