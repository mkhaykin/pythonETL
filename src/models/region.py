from sqlalchemy import Column
from sqlalchemy.types import VARCHAR

from .base import BaseModel


class Region(BaseModel):
    name = Column(
        VARCHAR(50),
        unique=True,
        nullable=False,
    )
