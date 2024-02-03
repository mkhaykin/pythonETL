from collections.abc import AsyncGenerator

from dotenv import dotenv_values
from sqlalchemy import Engine
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.models import Base

settings = dotenv_values("./../.env")

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings["POSTGRES_USER"],
    password=settings["POSTGRES_PASSWORD"],
    host=settings["POSTGRES_HOST"],
    port=settings["POSTGRES_PORT"],  # type: ignore
    database=settings["POSTGRES_DB"],
)

SQLALCHEMY_DATABASE_URL_async = URL.create(
    drivername="postgresql+asyncpg",
    username=settings["POSTGRES_USER"],
    password=settings["POSTGRES_PASSWORD"],
    host=settings["POSTGRES_HOST"],
    port=settings["POSTGRES_PORT"],  # type: ignore
    database=settings["POSTGRES_DB"],
)


def get_engine() -> Engine:
    return create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
    )


def get_async_engine() -> AsyncEngine:
    return create_async_engine(
        SQLALCHEMY_DATABASE_URL_async,
        pool_pre_ping=True,
        future=True,
    )


engine = get_engine()
async_engine = get_async_engine()


async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator:
    _async_engine = create_async_engine(
        url=SQLALCHEMY_DATABASE_URL_async,
        pool_pre_ping=True,
    )
    _session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with _session() as session:
        yield session

    await _async_engine.dispose()


async def async_create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def async_drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)
