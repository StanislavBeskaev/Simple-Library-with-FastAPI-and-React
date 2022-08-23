import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from backend import api_library
from backend.exceptions import LibraryValidationException
from backend.services.init_db import DBInitializer
from backend.services.ws_notifications import WSConnectionManager


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
    logger.info("Старт API")
    DBInitializer().init_db()


@app.exception_handler(LibraryValidationException)
async def library_validation_exception_handler(request, exc: LibraryValidationException):
    logger.warning(f"library_validation_exception_handler, исключение: {exc}")
    return JSONResponse(content=exc.errors, status_code=400)


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint websocket соединений для уведомлений"""
    manager = WSConnectionManager()
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(f"message from ws: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


fronted_build_folder = Path(os.path.join(Path(__file__).resolve().parent.parent, "frontend", "build"))
templates = Jinja2Templates(directory=fronted_build_folder.as_posix())

app.mount(
    "/static/",
    StaticFiles(directory=os.path.join(fronted_build_folder, "static")),
    name="React App static files",
)


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(request: Request, full_path: str):
    """Endpoint для отрисовки React приложения"""
    logger.debug(f"serve_react_app, full_path: {full_path}")
    return templates.TemplateResponse("index.html", {"request": request})
