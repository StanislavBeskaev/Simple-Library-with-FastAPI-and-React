from fastapi import APIRouter

from . import (
    authors,
    books,
)


router = APIRouter(
    prefix="/api_library"
)

router.include_router(authors.router)
router.include_router(books.router)

