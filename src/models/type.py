from sqlalchemy import Column
from sqlalchemy.types import VARCHAR

from .base import BaseModel


class Type(BaseModel):
    name = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
