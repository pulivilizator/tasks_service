from typing import AsyncIterator

from dishka import Provider, provide, Scope
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core.config.config import get_config, ConfigModel
from infrastructure.utils.i18n import create_translator_hub
from repository.implementations.bot_repository import BotRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    def get_bot_repository(self, r: Redis) -> BotRepository:
        return BotRepository(r=r)


