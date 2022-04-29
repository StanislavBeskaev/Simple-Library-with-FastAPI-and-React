import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .services.init_db import DBInitializer
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

app.mount('/', StaticFiles(directory=fronted_build_folder, html=True), name='frontend')
