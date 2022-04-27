from fastapi import APIRouter

from . import (
    authors,
)


router = APIRouter(
    prefix="/api_library"
)
router.include_router(authors.router)

