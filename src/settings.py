from dataclasses import dataclass
from os import environ

import dotenv


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


dotenv.load_dotenv(
    dotenv_path=".env",
    override=False,
)

settings = Settings(
    POSTGRES_USER=environ["POSTGRES_USER"],
    POSTGRES_PASSWORD=environ["POSTGRES_PASSWORD"],
    POSTGRES_HOST=environ["POSTGRES_HOST"],
    POSTGRES_PORT=int(environ["POSTGRES_PORT"]),
    POSTGRES_DB=environ["POSTGRES_DB"],
    TG_BOT_TOKEN=environ["TG_BOT_TOKEN"],
)
