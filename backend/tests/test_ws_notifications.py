from backend import tables
from backend.db.facade import DBFacade
from backend.models import AuthorCreate, BookUpdate, BookCreate
from backend.services.authors import AuthorsService
from backend.services.books import BooksService
from backend.services.ws_notifications import Notification, NotificationType
from backend.tests.base import BaseTestCase, override_get_session


test_authors = [
    tables.Author(id=1, name="Автор", surname="Первый", birth_year=1),

]

test_books = [
    tables.Book(id=1, name="Книга 1", author=1, isbn="isbn-1", issue_year=1111, page_count=11),
    tables.Book(id=2, name="Книга 2", author=1, isbn="isbn-2", issue_year=2222, page_count=12),
    tables.Book(id=3, name="Книга 3", author=1, isbn="isbn-3", issue_year=3333, page_count=13),
]


class TestWSNotifications(BaseTestCase):
    ws_notifications_url = "/ws/notifications"

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

    def test_author_create_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            test_db_facade = DBFacade(session=next(override_get_session()))
            author_service = AuthorsService(db_facade=test_db_facade)

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
            test_db_facade = DBFacade(session=next(override_get_session()))
            books_service = BooksService(db_facade=test_db_facade)

            book_to_delete = test_books[1]
            books_service.delete(book_id=book_to_delete.id)

            ws_data = websocket.receive_json()
            expected_notification = Notification(
                type=NotificationType.ERROR,
                text=f"Удалена книга {book_to_delete.name}"
            ).dict()

            self.assertEqual(ws_data, expected_notification)

    def test_book_update_notification(self):
        with self.client.websocket_connect(self.ws_notifications_url) as websocket:
            test_db_facade = DBFacade(session=next(override_get_session()))
            books_service = BooksService(db_facade=test_db_facade)

            book_to_update = test_books[1]
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
            test_db_facade = DBFacade(session=next(override_get_session()))
            books_service = BooksService(db_facade=test_db_facade)

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
