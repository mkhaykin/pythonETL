from typing import Any, ClassVar

import sqlalchemy as sa


class Mixin:  # for mypy
    __table__: ClassVar[sa.FromClause]
    __tablename__: Any


class MixinID(Mixin):
    id = sa.Column(
        sa.Integer,
        primary_key=True,
        nullable=False,
    )


class Base(sa.orm.DeclarativeBase):
    @sa.orm.declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base, MixinID):
    __abstract__ = True
