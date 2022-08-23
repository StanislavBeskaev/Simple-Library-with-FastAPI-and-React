from backend.db.mock.facade import MockDBFacade
from backend.db.mock.books import MockBooksDao
from backend.models import AuthorCreate, BookUpdate, BookCreate
from backend.services.authors import AuthorsService
from backend.services.books import BooksService
from backend.services.ws_notifications import Notification, NotificationType
from backend.tests.base import BaseLibraryTestCase


class TestWSNotifications(BaseLibraryTestCase):
    ws_notifications_url = "/ws/notifications"

    def test_author_create_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            author_service = AuthorsService(db_facade=MockDBFacade())

            new_author = AuthorCreate(
                name="Автор",
                surname="Новый",
                birth_year=1767
            )
            author_service.create(author_data=new_author)
            ws_data = websocket.receive_json()
            expected_notification = Notification(
                type=NotificationType.SUCCESS,
                text=f"Создан новый автор: {new_author.name} {new_author.surname}, {new_author.birth_year}"
            ).dict()

            self.assertEqual(ws_data, expected_notification)

    def test_book_delete_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            books_service = BooksService(db_facade=MockDBFacade())

            books_service.delete(book_id=1)

            ws_data = websocket.receive_json()
            expected_notification = Notification(
                type=NotificationType.ERROR,
                text=f"Удалена книга рассказ 1"
            ).dict()

            self.assertEqual(ws_data, expected_notification)

    def test_book_update_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            books_service = BooksService(db_facade=MockDBFacade())
            mock_books_dao = MockBooksDao()
            book_to_update = mock_books_dao.test_books[1]

            books_service.update(
                book_id=book_to_update.id,
                book_data=BookUpdate(
                    name=book_to_update.name,
                    author=book_to_update.author,
                    isbn=book_to_update.isbn,
                    issue_year=1703,
                    page_count=3
                )
            )

            ws_data = websocket.receive_json()
            expected_notification = Notification(
                type=NotificationType.WARNING,
                text=f"Изменена книга {book_to_update.name}"
            ).dict()

            self.assertEqual(ws_data, expected_notification)

    def test_book_create_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            books_service = BooksService(db_facade=MockDBFacade())

            book_to_create = BookCreate(
                name="Новая книга",
                author=1,
                isbn="new-isbn",
                issue_year=1583,
                page_count=1171
            )
            books_service.create(book_data=book_to_create)

            ws_data = websocket.receive_json()
            expected_notification = Notification(
                type=NotificationType.SUCCESS,
                text=f"Создана новая книга: {book_to_create.name}"
            ).dict()

            self.assertEqual(ws_data, expected_notification)
