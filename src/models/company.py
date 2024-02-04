from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.types import VARCHAR

from .base import BaseModel


class Company(BaseModel):
    name = Column(
        VARCHAR(250),
        nullable=False,
    )

    inn = Column(
        VARCHAR(12),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("name", "inn", name="uc_company"),)
