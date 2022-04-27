from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import api_library
from .database import engine
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


@app.get("/")
async def root():
    return {"message": "Hello World"}
