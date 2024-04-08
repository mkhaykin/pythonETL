import asyncio
import logging
import sys

from bot import bot_loop
from db import create_tables, drop_tables
from xlsx import import_xlsx

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Bot start")
    drop_tables()
    create_tables()

    import_xlsx()
    # export_xlsx()

    asyncio.run(bot_loop())
    logger.info("Bot finished")
