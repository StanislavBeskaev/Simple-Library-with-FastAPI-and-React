import json
import os
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


def init_db():
    logger.debug("run init_db")
    db_session = next(get_session())
    tables.Base.metadata.create_all(bind=engine)

    if not _is_authors_exist(session=db_session):
        logger.info("init_db загружаем данные в базу из файлов")

        load_authors_from_json(
            session=db_session,
            authors_file=init_file_path(AUTHORS_FILE)
        )

        load_books_from_json(
            session=db_session,
            books_file=init_file_path(BOOKS_FILE)
        )
    else:
        logger.info("init_db в базе уже есть данные")


def _is_authors_exist(session: Session) -> bool:
    authors_count = session.query(tables.Author).count()

    return authors_count > 0


def init_file_path(file_name: str) -> str:
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


def load_books_from_json(session: Session, books_file: str) -> None:
    books = parse_file_as(list[models.Book], books_file)

    for book in books:
        session.add(tables.Book(**book.dict()))

    session.commit()
    logger.info(f"Книги записаны в базу из файла {books_file}")

    _set_sequence_value(
        session=session,
        sequence_name="books_id_seq",
        restart_value=len(books) + 1
    )


def load_authors_from_json(session: Session, authors_file: str) -> None:
    authors = parse_file_as(list[models.Author], authors_file)

    for author in authors:
        session.add(tables.Author(**author.dict()))

    session.commit()
    logger.info(f"Авторы записаны в базу из файла {authors_file}")

    _set_sequence_value(
        session=session,
        sequence_name="authors_id_seq",
        restart_value=len(authors) + 1
    )


def _set_sequence_value(session: Session, sequence_name: str, restart_value: int) -> None:
    session.execute(f"alter sequence {sequence_name} restart with {restart_value}")
    session.commit()
    logger.info(f"Для последовательности {sequence_name} установлено значение {restart_value}")
