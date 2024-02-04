from sqlalchemy import Column
from sqlalchemy.types import VARCHAR

from .base import BaseModel


class Status(BaseModel):
    name = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
