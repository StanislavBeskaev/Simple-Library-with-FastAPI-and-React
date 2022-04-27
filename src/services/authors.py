from typing import (
    List,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class AuthorsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self):
        authors = (
            self.session
            .query(tables.Author)
            .order_by(tables.Author.id)
            .all()
        )

        return authors
