from typing import Any

from backend import models
from backend.db.mock.books import MockBooksDao
from backend.tests.base import BaseLibraryTestCase


test_books = MockBooksDao().test_books


class BaseTestBooks(BaseLibraryTestCase):
    books_url = "/api_library/books/"


class TestFindBooks(BaseTestBooks):
    def test_find_books_pagination(self):
        response = self.client.get(self.books_url, params={"page_size": 5, "page": 2})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books)
        expected_books_result = models.BookSearchResult(
            count=len(searched_books),
            results=searched_books[5:10]
        )
        self.assertEqual(response.json(), expected_books_result.dict())

        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books)
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"page_size": 10})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books)
        expected_books_result = models.BookSearchResult(
            count=len(searched_books),
            results=searched_books[:10]
        )
        self.assertEqual(response.json(), expected_books_result.dict())

    def _check_books_search_result(self, response_data: Any, searched_books: list[dict]):
        expected_books_result = models.BookSearchResult(
            count=len(searched_books),
            results=searched_books
        )
        self.assertEqual(response_data, expected_books_result.dict())

    def test_find_books_by_name(self):
        response = self.client.get(self.books_url, params={"name": "рассказ"})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[:5])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,

        )

        response = self.client.get(self.books_url, params={"name": "история"})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[5:10])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"name": "роман"})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[10:])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"name": 3})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[2::5])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

    def test_find_books_by_year(self):
        response = self.client.get(self.books_url, params={"issue_year__gte": 1700, "issue_year__lte": 1800})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[
            book for book in test_books if 1700 <= book.issue_year <= 1800
        ])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"issue_year__gte": 1590})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[book for book in test_books if 1590 <= book.issue_year])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"issue_year__lte": 1241})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[book for book in test_books if book.issue_year <= 1241])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

    def test_find_books_by_page_count(self):
        response = self.client.get(self.books_url, params={"page_count__gte": 17, "page_count__lte": 78})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[
            book for book in test_books if 17 <= book.page_count <= 79
        ])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"page_count__gte": 29})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[
            book for book in test_books if 29 <= book.page_count
        ])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"page_count__lte": 27})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=[
            book for book in test_books if book.page_count <= 27
        ])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

    def test_find_books_by_author(self):
        response = self.client.get(self.books_url, params={"author": 1})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[:5])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"author": 2})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[5:10])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
        )

        response = self.client.get(self.books_url, params={"author": 3})
        self.assertEqual(response.status_code, 200)
        searched_books = self.convert_to_dicts(items=test_books[10:])
        self._check_books_search_result(
            response_data=response.json(),
            searched_books=searched_books,
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

    def test_delete_book_success(self):
        response = self.client.delete(f"{self.books_url}1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), None)

        response = self.client.delete(f"{self.books_url}7")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), None)

        response = self.client.delete(f"{self.books_url}15")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json(), None)

    def test_delete_book_failed(self):
        response = self.client.delete(f"{self.books_url}16")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 16 not found"})

        response = self.client.delete(f"{self.books_url}123")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 123 not found"})

        response = self.client.delete(f"{self.books_url}12764")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 12764 not found"})

    def test_update_book_success(self):
        response = self.client.put(
            f"{self.books_url}1",
            json={
                "name": "рассказ_1",
                "author": 2,
                "isbn": "tale_isbn_1",
                "issue_year": 1205,
                "page_count": 11
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "name": "рассказ_1",
                "author": 2,
                "isbn": "tale_isbn_1",
                "issue_year": 1205,
                "page_count": 11,
                "id": 1
            }
        )

    def test_update_book_not_found(self):
        response = self.client.put(
            f"{self.books_url}16",
            json={
                "name": "рассказ_1",
                "author": 2,
                "isbn": "tale_isbn_1",
                "issue_year": 1205,
                "page_count": 11
            }
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Book with id 16 not found"})

    def test_update_book_failed(self):
        response = self.client.put(
            f"{self.books_url}1",
            json={
                "name": "рассказ 2",
                "author": 2,
                "isbn": "tale-isbn-3",
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

        response = self.client.put(
            f"{self.books_url}1",
            json={
                "name": "рассказ 2",
                "author": 2,
                "isbn": "tale-isbn-3",
                "issue_year": -2,
                "page_count": 15
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует',
                'isbn': 'Книга с таким ISBN уже существует',
                'issue_year': 'Год выпуска должен быть больше 0'
            }
        )

        response = self.client.put(
            f"{self.books_url}1",
            json={
                "name": "рассказ 2",
                "author": 2,
                "isbn": "tale-isbn-3",
                "issue_year": 1565,
                "page_count": 15
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

        response = self.client.put(
            f"{self.books_url}1",
            json={
                "name": "рассказ 2",
                "author": 2,
                "isbn": "tale_isbn_1",
                "issue_year": 1565,
                "page_count": 15
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'name': 'Книга с таким названием уже существует'
            }
        )
