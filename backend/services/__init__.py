from abc import ABC

from fastapi import Depends

from backend.db.facade import DBFacadeInterface, get_db_facade


class BaseService(ABC):
    """Базовый сервис, инициализация фасада базы данных"""
    def __init__(self, db_facade: DBFacadeInterface = Depends(get_db_facade)):
        self.db_facade = db_facade
