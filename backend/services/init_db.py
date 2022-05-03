import os
import random
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from loguru import logger
from pydantic import parse_file_as, BaseModel
from sqlalchemy.orm import Session

from .. import models
from .. import tables
from ..database import engine, get_session
from ..settings import get_settings


INIT_DATA_TYPE_VAR = "INIT_DATA_TYPE"
JSON_INIT_DATA_TYPE_PREFIX = "json"
TEST_INIT_DATA_TYPE_PREFIX = "test"  # в формате test_<кол-во авторов>_<кол-во книг>


class DBInitializer:
    """Класс для инициализации базы и заполнения начальными данными"""

    def __init__(self):
        self.session = next(get_session())

    def init_db(self):
        tables.Base.metadata.create_all(bind=engine)

        init_data_type = get_settings().init_data_type
        logger.debug(f"{init_data_type=}")

        if not self._need_load_data():
            logger.info("init_db в базе уже есть данные")
            return

        logger.info("init_db база пустая")

        if not init_data_type:
            logger.info(f"Не задана переменная окружения {INIT_DATA_TYPE_VAR}."
                        f" Начальные данные в базу не загружаются")
            return

        if init_data_type.startswith(JSON_INIT_DATA_TYPE_PREFIX):
            logger.info("init_db загружаем данные в базу из json файлов")
            json_init_data_loader = JsonInitDataLoader(session=self.session, init_data_type=init_data_type)
            json_init_data_loader.load_init_data()
        elif init_data_type.startswith(TEST_INIT_DATA_TYPE_PREFIX):
            logger.info("Генерируем тестовых авторов и книги")
            test_init_data_loader = TestInitDataLoader(session=self.session, init_data_type=init_data_type)
            test_init_data_loader.load_init_data()
        else:
            message = f"Неожиданное значение для переменной окружения {INIT_DATA_TYPE_VAR} передано значение " \
                      f" '{init_data_type}', должно начинаться" \
                      f" с {JSON_INIT_DATA_TYPE_PREFIX} или {TEST_INIT_DATA_TYPE_PREFIX}"
            logger.error(message)
            raise ValueError(message)

    def _need_load_data(self) -> bool:
        authors_count = self.session.query(tables.Author).count()

        return authors_count == 0


class BaseInitDataLoader(ABC):
    """Базовый класс для загрузки первоначальных данных в базу"""

    def __init__(self, session: Session, init_data_type: str):
        self.session = session
        self.init_data_type = init_data_type

    @abstractmethod
    def load_init_data(self) -> None:
        pass


@dataclass
class TableLoadParam:
    """Параметры для загрузки данных таблицы из json"""
    init_file: str  # название файла в папке с начальными данными
    model: BaseModel
    table: tables.Base
    sequence_name: str


class JsonInitDataLoader(BaseInitDataLoader):
    """Класс для загрузки первоначальных данных в базу из json файлов"""
    INIT_DATA_FOLDER_PATH = os.path.join(Path(__file__).resolve().parent.parent, "init_data")
    INIT_DATA_TABLE_LOAD_PARAMS = [
        TableLoadParam(
            init_file="authors.json",
            model=models.Author,
            table=tables.Author,
            sequence_name="authors_id_seq"
        ),
        TableLoadParam(
            init_file="books.json",
            model=models.Book,
            table=tables.Book,
            sequence_name="books_id_seq"
        ),
    ]

    def load_init_data(self) -> None:
        """Загрузка первоначальных данных таблиц из json файлов"""
        for table_load_param in self.INIT_DATA_TABLE_LOAD_PARAMS:
            self._load_table_data_with_load_param(table_load_param=table_load_param)

    def _load_table_data_with_load_param(self, table_load_param: TableLoadParam):
        """Загрузка данных в таблицу по указанным параметрам"""
        table_init_file_path = self._get_table_data_init_file_path(table_load_param.init_file)
        table_models = parse_file_as(
            list[table_load_param.model],
            table_init_file_path
        )

        for table_model in table_models:
            self.session.add(table_load_param.table(**table_model.dict()))

        self.session.commit()
        logger.info(f"Загружено {len(table_models)} строк в таблицу {table_load_param.table}"
                    f" из файла {table_init_file_path}")

        self._set_sequence_value(
            sequence_name=table_load_param.sequence_name,
            restart_value=len(table_models) + 1
        )

    def _get_table_data_init_file_path(self, file_name: str) -> str:
        """Получение пути до файла с первоначальными данными таблицы"""
        return os.path.join(self.INIT_DATA_FOLDER_PATH, file_name)

    def _set_sequence_value(self, sequence_name: str, restart_value: int) -> None:
        """Установка перезапуск последовательности с указанного значения"""
        self.session.execute(f"alter sequence {sequence_name} restart with {restart_value}")
        self.session.commit()
        logger.info(f"Для последовательности {sequence_name} установлено значение {restart_value}")


class TestInitDataLoader(BaseInitDataLoader):
    """Класс для загрузки тестовых первоначальных данных в базу"""

    def __init__(self, session: Session, init_data_type: str):
        super().__init__(session=session, init_data_type=init_data_type)

        self.authors_amount, self.books_amount = self._parse_test_init_data_type()

    def _parse_test_init_data_type(self) -> tuple[int, int]:
        """Парсинг тестового типа инициализации данных, валидация и выделения кол-ва авторов и книг"""
        pattern = r"^test_(?P<authors>\d+)_(?P<books>\d+)$"

        match_amounts = re.match(pattern=pattern, string=self.init_data_type)
        if not match_amounts:
            raise ValueError(
                f"Не удалось получить кол-во авторов и книг из значения переменной окружения {INIT_DATA_TYPE_VAR},"
                f" передано значение '{self.init_data_type}'. Должен быть формат: test_<кол-во авторов>_<кол-во книг>"
            )

        authors_amount = int(match_amounts.group("authors"))
        books_amount = int(match_amounts.group("books"))
        if any([amount == 0 for amount in (authors_amount, books_amount)]):
            raise ValueError(
                f"Не удалось получить кол-во авторов и книг из значения переменной окружения {INIT_DATA_TYPE_VAR},"
                f" передано значение '{self.init_data_type}'. Нужно указать положительные количества авторов и книг"
            )

        return authors_amount, books_amount

    def load_init_data(self) -> None:
        """Загрузка первоначальных тестовых данных таблиц"""
        self._generate_test_authors()
        self._generate_test_books()

    def _generate_test_authors(self) -> None:
        """Генерация тестовых данных по авторам"""
        logger.debug(f"Генерируем {self.authors_amount} тестовых авторов")
        test_authors = [
            tables.Author(
                name=f"Имя тестового автора {i}",
                surname=f"Фамилия тестового автора {i}",
                birth_year=random.randrange(1, 2001)
            ) for i in range(1, self.authors_amount + 1)
        ]
        logger.debug(f"Сформирован список {self.authors_amount} авторов для вставки в базу")
        self.session.bulk_save_objects(test_authors)
        self.session.commit()
        logger.info(f"Сгенерировано {self.authors_amount} тестовых авторов")

    def _generate_test_books(self) -> None:
        """Генерация тестовых данных по книгам"""
        logger.debug(f"Генерируем {self.books_amount} тестовых книг")
        test_books = [
            tables.Book(
                name=f"Тестовая книга {i}",
                author=random.randrange(1, self.authors_amount + 1),
                isbn=f"test_isbn_{i}",
                issue_year=random.randrange(1, 1991),
                page_count=random.randrange(1, 749)
            ) for i in range(1, self.books_amount + 1)
        ]
        logger.debug(f"Сформирован список {self.books_amount} книг для вставки в базу")
        self.session.bulk_save_objects(test_books)
        self.session.commit()
        logger.info(f"Сгенерировано {self.books_amount} тестовых книг")
