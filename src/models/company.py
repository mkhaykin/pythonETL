import sqlalchemy as sa

from .base import BaseModel


class Company(BaseModel):
    name = sa.Column(
        sa.types.VARCHAR(250),
        nullable=False,
    )

    inn = sa.Column(
        sa.types.VARCHAR(12),
        nullable=False,
    )

    __table_args__ = (sa.UniqueConstraint("name", "inn", name="uc_company"),)
