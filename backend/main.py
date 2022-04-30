import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .services.init_db import DBInitializer
from .services.ws_notifications import WSConnectionManager
from . import api_library
from .exceptions import LibraryValidationException


app = FastAPI(
        title='API Библиотеки',
        description='Работа с книгами и авторами',
        version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_library.router)


@app.on_event("startup")
def initialize_db():
    DBInitializer().init_db()


@app.exception_handler(LibraryValidationException)
async def library_validation_exception_handler(request, exc: LibraryValidationException):
    return JSONResponse(content=exc.errors, status_code=400)


fronted_build_folder = os.path.join(Path(__file__).resolve().parent.parent, "frontend", "build")
static_files_folder = os.path.join(fronted_build_folder, "static")

app.mount('/static', StaticFiles(directory=static_files_folder), name='static')


@app.get("/")
def index():
    # если делать mount всей папки build, то не работают ws
    with open(os.path.join(fronted_build_folder, "index.html"), mode="r") as file:
        content = file.read()
    return HTMLResponse(content)


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    manager = WSConnectionManager()
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"message from ws: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
