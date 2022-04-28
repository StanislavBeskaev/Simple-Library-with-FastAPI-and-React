from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from . import api_library
from .db_data_handlers import init_db
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
    init_db()


@app.exception_handler(LibraryValidationException)
async def library_validation_exception_handler(request, exc: LibraryValidationException):
    return JSONResponse(content=exc.errors, status_code=400)
