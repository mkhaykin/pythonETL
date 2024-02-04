import asyncio

from src.bot import bot_loop
from src.db import create_tables, drop_tables
from src.xlsx import import_xlsx

if __name__ == "__main__":
    drop_tables()
    create_tables()

    import_xlsx()
    # export_xlsx()

    asyncio.run(bot_loop())
