import json
import os
import random
from pathlib import Path

from loguru import logger
from pydantic import parse_file_as
from sqlalchemy.orm import Session

from .database import get_session, engine
from . import tables
from . import models


INIT_DATA_FOLDER_PATH = os.path.join(Path(__file__).resolve().parent, "init_data")
AUTHORS_FILE = "authors.json"
BOOKS_FILE = "books.json"

INIT_DATA_TYPE_VAR = "INIT_DATA_TYPE"
TEST_INIT_DATA_PREFIX = "test"  # в формате test_<кол-во авторов>_<кол-во книг>
JSON_INIT_DATA_PREFIX = "json"


def init_db():
    logger.debug("run init_db")
    db_session = next(get_session())
    tables.Base.metadata.create_all(bind=engine)

    if _is_authors_exist(session=db_session):
        logger.info("init_db в базе уже есть данные")
        return

    logger.info("init_db база пустая")

    init_data_type = os.environ.get(INIT_DATA_TYPE_VAR)
    if not init_data_type:
        logger.info(f"Не задана переменная окружения {INIT_DATA_TYPE_VAR}. Начальные данные в базу не загружаются")
        return

    if init_data_type.startswith(JSON_INIT_DATA_PREFIX):
        logger.info("init_db загружаем данные в базу из файлов")
        _load_data_from_init_files(session=db_session)
    elif init_data_type.startswith(TEST_INIT_DATA_PREFIX):
        logger.info("Генерируем тестовых авторов и книги")
        _generate_test_data(session=db_session, init_data_type=init_data_type)
    else:
        message = f"Неожиданное значение для переменной окружения {INIT_DATA_TYPE_VAR} передано значение " \
                  f" {init_data_type}, должно начинаться" \
                  f" с {JSON_INIT_DATA_PREFIX} или {TEST_INIT_DATA_PREFIX}"
        logger.error(message)
        raise ValueError(message)


def _is_authors_exist(session: Session) -> bool:
    authors_count = session.query(tables.Author).count()

    return authors_count > 0


def _load_data_from_init_files(session: Session) -> None:
    load_authors_from_json(
        session=session,
        authors_file=_get_init_file_path(AUTHORS_FILE)
    )

    load_books_from_json(
        session=session,
        books_file=_get_init_file_path(BOOKS_FILE)
    )


def _get_init_file_path(file_name: str) -> str:
    return os.path.join(INIT_DATA_FOLDER_PATH, file_name)


def save_authors_from_db(session: Session, authors_file: str) -> None:
    authors = [models.Author.from_orm(author).dict() for author in session.query(tables.Author).all()]
    logger.info("Получили авторов из базы")

    with open(authors_file, mode='w', encoding='utf-8') as file:
        json.dump(obj=authors, fp=file, indent=2, ensure_ascii=False)

    logger.info(f"Авторы сохранены в файл {authors_file}")


def save_books_from_db(session: Session, books_file: str) -> None:
    books = [models.Book.from_orm(book).dict() for book in session.query(tables.Book).all()]
    logger.info("Получили книги из базы")

    with open(books_file, mode='w', encoding='utf-8') as file:
        json.dump(obj=books, fp=file, indent=2, ensure_ascii=False)

    logger.info(f"Книги сохранены в файл {books_file}")


def load_authors_from_json(session: Session, authors_file: str) -> None:
    authors = parse_file_as(list[models.Author], authors_file)

    for author in authors:
        session.add(tables.Author(**author.dict()))

    session.commit()
    logger.info(f"Загружено {len(authors)} авторов в базу из файла {authors_file}")

    _set_sequence_value(
        session=session,
        sequence_name="authors_id_seq",
        restart_value=len(authors) + 1
    )


def load_books_from_json(session: Session, books_file: str) -> None:
    books = parse_file_as(list[models.Book], books_file)

    for book in books:
        session.add(tables.Book(**book.dict()))

    session.commit()
    logger.info(f"Загружено {len(books)} книг в базу из файла {books_file}")

    _set_sequence_value(
        session=session,
        sequence_name="books_id_seq",
        restart_value=len(books) + 1
    )


def _set_sequence_value(session: Session, sequence_name: str, restart_value: int) -> None:
    session.execute(f"alter sequence {sequence_name} restart with {restart_value}")
    session.commit()
    logger.info(f"Для последовательности {sequence_name} установлено значение {restart_value}")


def _generate_test_data(session: Session, init_data_type: str) -> None:
    # TODO заменить на регулярочку и функцию выделения количеств
    init_data_type_parts = init_data_type.split("_")
    if len(init_data_type_parts) != 3:
        message = f"Некорректное значение для переменной окружения {INIT_DATA_TYPE_VAR}, передано значение {init_data_type}" \
                  f", для типа {TEST_INIT_DATA_PREFIX} должен быть формат: test_<кол-во авторов>_<кол-во книг>"
        logger.error(message)
        raise ValueError(message)

    try:
        authors_amount = int(init_data_type_parts[1])
        books_amount = int(init_data_type_parts[2])
    except ValueError:
        message = f"Не удалось получить кол-во авторов и книг из значения переменной окружения {INIT_DATA_TYPE_VAR}," \
                  f" передано значение {init_data_type}. Должен быть формат: test_<кол-во авторов>_<кол-во книг>"
        raise ValueError(message)

    _generate_test_authors(session=session, authors_amount=authors_amount)
    _generate_test_books(session=session, books_amount=books_amount, authors_amount=authors_amount)


def _generate_test_authors(session: Session, authors_amount: int) -> None:
    for i in range(1, authors_amount + 1):
        session.add(
            tables.Author(
                name=f"Имя тестового автора {i}",
                surname=f"Фамилия тестового автора {i}",
                birth_year=random.randrange(1, 2000)
            )
        )
    session.commit()
    logger.info(f"Сгенерировано {authors_amount} тестовых авторов")


def _generate_test_books(session: Session, books_amount: int, authors_amount: int) -> None:
    for i in range(1, books_amount + 1):
        session.add(
            tables.Book(
                name=f"Тестовая книга {i}",
                author=random.randrange(1, authors_amount),
                isbn=f"test_isbn_{i}",
                issue_year=random.randrange(1, 1991),
                page_count=random.randrange(1, 749)
            )
        )
    session.commit()
    logger.info(f"Сгенерировано {books_amount} тестовых книг")
