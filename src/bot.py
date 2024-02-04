from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message
from dotenv import dotenv_values

from src.xlsx import export_xlsx

settings = dotenv_values("./../.env")
TOKEN: str = settings["TG_BOT_TOKEN"]  # type: ignore
FILE_TO_EXPORT = "./../export/send.xlsx"

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        text="Hi! Enter '/report'",
    )


@dp.message(Command("report"))
async def report_handler(message: types.Message):
    """
    This handler receives messages with `/report` command
    """
    export_xlsx()

    await message.answer_document(
        document=FSInputFile(
            path=FILE_TO_EXPORT,
            filename="report.xlsx",
        ),
    )


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def bot_loop() -> None:
    bot = Bot(
        token=TOKEN,
        parse_mode=ParseMode.HTML,
    )
    await dp.start_polling(bot)