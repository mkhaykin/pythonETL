import asyncio

from bot import bot_loop
from db import create_tables, drop_tables
from xlsx import import_xlsx

if __name__ == "__main__":
    drop_tables()
    create_tables()

    import_xlsx()
    # export_xlsx()

    asyncio.run(bot_loop())
