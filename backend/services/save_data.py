import json

from loguru import logger
from sqlalchemy.orm import Session

from .. import tables
from .. import models


# TODO реализовать сервис для получения json файлов с данными таблиц


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
