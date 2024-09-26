from typing import AsyncIterator

from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientSession
from dishka import Provider, provide, Scope
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core.config.config import get_config, ConfigModel
from infrastructure.utils.i18n import create_translator_hub


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> ConfigModel:
        return get_config()

    @provide(scope=Scope.APP)
    async def get_redis(self, config: ConfigModel) -> AsyncIterator[Redis]:
        r = Redis.from_url(config.redis.dsn.unicode_string())
        yield r
        await r.aclose()

    @provide(scope=Scope.APP)
    def get_translator_hub(self) -> TranslatorHub:
        translator_hub = create_translator_hub()
        return translator_hub

    @provide(scope=Scope.APP)
    async def get_session(self) -> AsyncIterator[ClientSession]:
        async with ClientSession() as session:
            yield session


