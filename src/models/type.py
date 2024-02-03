import sqlalchemy as sa

from .base import BaseModel


class Type(BaseModel):
    name = sa.Column(
        sa.types.VARCHAR(50),
        unique=True,
        nullable=False,
    )
