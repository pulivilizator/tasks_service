import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs

from dishka.integrations.aiogram import setup_dishka

import logging

from redis.asyncio import Redis

from bot.core.dishka_container import make_dishka_container
from core.config.config import get_config
from application import get_routers

logging.basicConfig(level=logging.INFO)

async def main():
    config = get_config()
    r = Redis()
    storage = RedisStorage(redis=r, key_builder=DefaultKeyBuilder(with_destiny=True))
    dp = Dispatcher(storage=storage)

    dp.include_routers(*get_routers())
    container = make_dishka_container()
    setup_dishka(container, dp, auto_inject=True)
    setup_dialogs(dp)
    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())