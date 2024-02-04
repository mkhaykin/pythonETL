from typing import Any, ClassVar

from sqlalchemy import Column, FromClause, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Mixin:  # for mypy
    __table__: ClassVar[FromClause]
    __tablename__: Any


class MixinID(Mixin):
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base, MixinID):
    __abstract__ = True
