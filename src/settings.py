from dotenv import dotenv_values
from dataclasses import dataclass


@dataclass
class Settings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    TG_BOT_TOKEN: str

    FILE_TO_EXPORT: str = "export/send.xlsx"
    FILE_TO_LOAD: str = "import/Просрочено (06.09.2022).xlsx"

    TMP_TABLE = "overdue_import"


settings = Settings(**dotenv_values(".env"))
