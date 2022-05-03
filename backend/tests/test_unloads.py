import json

from .. import models
from .test_books import BaseTestBooks, test_books, test_authors


class TestUnloads(BaseTestBooks):

    def test_authors_unload(self):
        response = self.client.get("/api_library/unloads/authors")
        self.assertEqual(response.status_code, 200)
        authors_unload = json.loads(response.content.decode())
        expected_unload = self.convert_to_dicts(items=test_authors, model=models.Author)
        self.assertEqual(authors_unload, expected_unload)

    def test_books_unload(self):
        response = self.client.get("/api_library/unloads/books")
        self.assertEqual(response.status_code, 200)
        books_unload = json.loads(response.content.decode())
        expected_unload = self.convert_to_dicts(items=test_books)
        self.assertEqual(books_unload, expected_unload)

        response = self.client.get("/api_library/unloads/books", params={"author": 2})
        self.assertEqual(response.status_code, 200)
        books_unload = json.loads(response.content.decode())
        expected_unload = self.convert_to_dicts(items=[book for book in test_books if book.author == 2])
        self.assertEqual(books_unload, expected_unload)

        response = self.client.get("/api_library/unloads/books", params={"name": "рассказ"})
        self.assertEqual(response.status_code, 200)
        books_unload = json.loads(response.content.decode())
        expected_unload = self.convert_to_dicts(items=test_books[:5])
        self.assertEqual(books_unload, expected_unload)
