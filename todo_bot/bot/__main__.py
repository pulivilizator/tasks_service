import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs

from dishka.integrations.aiogram import setup_dishka, AutoInjectMiddleware, ContainerMiddleware

import logging

from redis.asyncio import Redis

from bot.core.dishka_container import make_dishka_container
from core.config.config import get_config
from application import get_routers
from core.consumer import handle_register
from core.menu import set_menu
from infrastructure.middlewares.i18n import TranslatorRunnerMiddleware
from infrastructure.middlewares.register_middleware import RegisterMiddleware

logging.basicConfig(level=logging.INFO)

async def main():
    config = get_config()
    r = Redis.from_url(config.redis.dsn.unicode_string())
    storage = RedisStorage(redis=r, key_builder=DefaultKeyBuilder(with_destiny=True))
    dp = Dispatcher(storage=storage)
    dp.include_routers(*get_routers())
    dp.startup.register(set_menu)

    container = make_dishka_container()
    setup_dishka(container, dp, auto_inject=True)

    dp.update.middleware(RegisterMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())

    setup_dialogs(dp)
    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(dp.start_polling(bot), handle_register(bot, dishka_container=container))

if __name__ == '__main__':
    asyncio.run(main())