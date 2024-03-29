from fastapi import APIRouter

from backend.api_library import (
    authors,
    books,
    unloads,
)


router = APIRouter(
    prefix="/api_library"
)

router.include_router(authors.router)
router.include_router(books.router)
router.include_router(unloads.router)

