from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import DATE, INTEGER, VARCHAR

from .base import BaseModel
from .company import Company
from .region import Region
from .status import Status
from .type import Type


class Overdue(BaseModel):
    region_id = Column(BaseModel.id.type, ForeignKey(Region.id))

    company_id = Column(
        BaseModel.id.type,
        ForeignKey(Company.id),
    )

    status_id = Column(BaseModel.id.type, ForeignKey(Status.id))

    type_id = Column(
        BaseModel.id.type,
        ForeignKey(Type.id),
    )

    gtin = Column(
        VARCHAR(14),
        nullable=False,
    )

    series = Column(
        VARCHAR(30),
        nullable=False,
    )

    doses = Column(
        INTEGER,
        nullable=False,
    )

    count_packs = Column(
        INTEGER,
        nullable=False,
    )

    count_doses = Column(
        INTEGER,
        nullable=False,
    )

    expiration_date = Column(
        DATE,
        nullable=False,
    )

    days_overdue = Column(
        INTEGER,
        nullable=False,
    )
