import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.handlers import start_handler
from src.configuration import conf


async def run_bot():
    bot: Bot = Bot(token=conf.bot.token, parse_mode='HTML')

    storage = MemoryStorage()

    dp: Dispatcher = Dispatcher(storage=storage)

    dp.include_router(start_handler.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(run_bot())
