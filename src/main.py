from fastapi import FastAPI

from . import api_library
from .database import engine
from .tables import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='API Библиотеки',
    description='Получение книг и авторов',
    version='0.1.0',
)

app.include_router(api_library.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
