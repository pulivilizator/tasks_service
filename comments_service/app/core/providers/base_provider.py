from typing import AsyncIterator

from aiohttp import ClientSession
from dishka import Provider, provide, Scope
from redis.asyncio import Redis

from core.config.config import get_config, ConfigModel
from services.comments_service import CommentsService


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
    async def get_client_session(self) -> AsyncIterator[ClientSession]:
        async with ClientSession() as session:
            yield session


