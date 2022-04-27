from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from . import api_library
from .database import engine
from .exceptions import LibraryValidationException
from .tables import Base


Base.metadata.create_all(bind=engine)

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


@app.exception_handler(LibraryValidationException)
async def library_validation_exception_handler(request, exc: LibraryValidationException):
    return JSONResponse(content=exc.errors, status_code=400)
