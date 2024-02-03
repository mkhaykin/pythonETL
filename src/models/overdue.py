import sqlalchemy as sa

from .base import BaseModel
from .company import Company
from .region import Region
from .status import Status
from .type import Type


class Overdue(BaseModel):
    region_id = sa.Column(BaseModel.id.type, sa.ForeignKey(Region.id))

    company_id = sa.Column(
        BaseModel.id.type,
        sa.ForeignKey(Company.id),
    )

    status_id = sa.Column(BaseModel.id.type, sa.ForeignKey(Status.id))

    type_id = sa.Column(
        BaseModel.id.type,
        sa.ForeignKey(Type.id),
    )

    gtin = sa.Column(
        sa.types.VARCHAR(14),
        nullable=False,
    )

    series = sa.Column(
        sa.types.VARCHAR(30),
        nullable=False,
    )

    doses = sa.Column(
        sa.types.INTEGER,
        nullable=False,
    )

    count_packs = sa.Column(
        sa.types.INTEGER,
        nullable=False,
    )

    count_doses = sa.Column(
        sa.types.INTEGER,
        nullable=False,
    )

    expiration_date = sa.Column(
        sa.types.DATE,
        nullable=False,
    )

    days_overdue = sa.Column(
        sa.types.INTEGER,
        nullable=False,
    )
