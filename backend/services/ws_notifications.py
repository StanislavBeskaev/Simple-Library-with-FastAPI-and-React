import asyncio
from enum import Enum

from fastapi import WebSocket
from loguru import logger
from pydantic import BaseModel


class NotificationType(str, Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'


class Notification(BaseModel):
    type: NotificationType
    text: str


class WSConnectionManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            logger.info(f"Создан instance {cls.__name__}")
            cls.__instance = super().__new__(cls)
        else:
            logger.debug(f"Взят текущий экземпляр {cls.__name__}")

        return cls.__instance

    def __init__(self):
        if not hasattr(self, "active_connections"):
            self.active_connections: list[WebSocket] = []

    def send_notification(self, notification: Notification):
        asyncio.run(self.broadcast(notification=notification))

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.debug(f"{self.__class__.__name__} новое ws соединение,"
                     f" в списке уже {len(self.active_connections)} соединений")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # TODO возможно этот метод не нужен
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, notification: Notification):
        logger.debug(f"{self.__class__.__name__}.broadcast for {len(self.active_connections)=} connection,"
                     f" send notification: {notification}")
        for connection in self.active_connections:
            await connection.send_json(notification.dict())
