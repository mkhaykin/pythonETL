import sqlalchemy as sa

from .base import BaseModel


class Status(BaseModel):
    name = sa.Column(
        sa.types.VARCHAR(50),
        unique=True,
        nullable=False,
    )
