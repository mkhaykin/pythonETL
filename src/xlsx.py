import logging

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import and_, column, exists, func, insert, or_, select

import models
from db import get_engine
from settings import settings

names = [
    "region_name",
    "company_name",
    "company_inn",
    "status",
    "type",
    "gtin",
    "series",
    "doses",
    "count_packs",
    "count_doses",
    "expiration_date",
    "days_overdue",
]

dtypes = {
    "region_name": models.Region.name.type,
    "company_name": models.Company.name.type,
    "company_inn": models.Company.inn.type,
    "status": models.Status.name.type,
    "type": models.Status.name.type,
    "gtin": models.Overdue.gtin.type,
    "series": models.Overdue.series.type,
    "doses": models.Overdue.doses.type,
    "count_packs": models.Overdue.count_packs.type,
    "count_doses": models.Overdue.count_doses.type,
    "expiration_date": models.Overdue.expiration_date.type,
    "days_overdue": models.Overdue.days_overdue.type,
}

logger = logging.getLogger(__name__)


def _from_xlsx_to_tmp():
    df = pd.read_excel(
        io=settings.FILE_TO_LOAD,
        sheet_name="Статика",
        header=None,
        names=names,
        skiprows=5,
        converters={
            "expiration_date": lambda x: pd.to_datetime(x, dayfirst=True)
        },
    )

    with get_engine().connect() as con:
        df.to_sql(
            name=settings.TMP_TABLE,
            con=con,
            schema="public",
            dtype=dtypes,
            if_exists="replace",
            method="multi",
        )


def _from_tmp_to_tables():
    # добавляем несуществующие регионы
    insert_region_stmt = insert(models.Region).from_select(
        names=[models.Region.name],
        select=(
            select(column("region_name").label("name"))
            .select_from(sa.table(settings.TMP_TABLE))
            .distinct()
            .filter(
                ~exists().where(column("region_name") == models.Region.name)
            )
        ),
    )

    # добавляем несуществующие статусы
    insert_status_stmt = insert(models.Status).from_select(
        names=[models.Status.name],
        select=(
            select(column("status").label("name"))
            .select_from(sa.table(settings.TMP_TABLE))
            .distinct()
            .filter(~exists().where(column("status") == models.Status.name))
        ),
    )

    # добавляем несуществующие типы
    insert_type_stmt = insert(models.Type).from_select(
        names=[models.Type.name],
        select=(
            select(column("type").label("name"))
            .select_from(sa.table(settings.TMP_TABLE))
            .distinct()
            .filter(~exists().where(column("type") == models.Type.name))
        ),
    )

    # добавляем не существующие организации
    insert_company_stmt = insert(models.Company).from_select(
        names=[models.Company.inn, models.Company.name],
        select=(
            select(
                column("company_inn").label("inn"),
                column("company_name").label("name"),
            )
            .select_from(sa.table(settings.TMP_TABLE))
            .distinct()
            .filter(
                ~exists().where(
                    or_(
                        column("company_inn") == models.Company.inn,
                        column("company_name") == models.Company.name,
                    )
                )
            )
        ),
    )

    # выборка из временной таблицы с привязкой к правильным внешним ключам
    select_stmt = (
        select(
            models.Region.id.label("region_id"),
            models.Company.id.label("company_id"),
            models.Status.id.label("status_id"),
            models.Type.id.label("type_id"),
            column("gtin"),
            column("series"),
            column("doses"),
            column("count_packs"),
            column("count_doses"),
            column("expiration_date"),
            column("days_overdue"),
        )
        .select_from(sa.table(settings.TMP_TABLE))
        .join(
            target=models.Company,
            onclause=and_(
                models.Company.inn == column("company_inn"),
                models.Company.name == column("company_name"),
            ),
        )
        .join(
            target=models.Region,
            onclause=models.Region.name == column("region_name"),
        )
        .join(
            target=models.Status,
            onclause=models.Status.name == column("status"),
        )
        .join(target=models.Type, onclause=models.Type.name == column("type"))
    )

    # заливаем в основную таблицу
    insert_overdue_stmt = insert(models.Overdue).from_select(
        names=[
            models.Overdue.region_id,
            models.Overdue.company_id,
            models.Overdue.status_id,
            models.Overdue.type_id,
            models.Overdue.gtin,
            models.Overdue.series,
            models.Overdue.doses,
            models.Overdue.count_packs,
            models.Overdue.count_doses,
            models.Overdue.expiration_date,
            models.Overdue.days_overdue,
        ],
        select=select_stmt,
    )

    with get_engine().connect() as con:
        con.execute(insert_region_stmt)
        con.execute(insert_status_stmt)
        con.execute(insert_type_stmt)
        con.execute(insert_company_stmt)
        con.execute(insert_overdue_stmt)
        con.commit()


def _from_table_to_xlsx():
    select_stmt = (
        select(
            models.Region.name,
            func.sum(models.Overdue.count_doses).label("sum_count_packs"),
            func.round(func.avg(models.Overdue.days_overdue)).label(
                "avg_days_overdue"
            ),
        )
        .join(
            target=models.Region,
        )
        .group_by(
            models.Region.name,
        )
        .order_by(models.Region.name)
    )

    with get_engine().connect() as con:
        df = pd.read_sql(
            sql=select_stmt,
            con=con,
        )
        df.to_excel(
            settings.FILE_TO_EXPORT,
            sheet_name="result",
            index=False,
            header=[
                "Субъект РФ",
                "Количество Доз",
                "Просрочено дней",
            ],
        )


def import_xlsx() -> None:
    logger.info("xlsx import start")
    _from_xlsx_to_tmp()
    _from_tmp_to_tables()
    logger.info("xlsx import finish")


def export_xlsx() -> None:
    logger.info("xlsx export start")
    _from_table_to_xlsx()
    logger.info("xlsx export finish")
