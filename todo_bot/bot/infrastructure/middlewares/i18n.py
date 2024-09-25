from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core.enums import Language
from repository.implementations.bot_repository import BotRepository
from .inject_middleware import aiogram_middleware_inject


class TranslatorRunnerMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
            hub: FromDishka[TranslatorHub],
            repository: FromDishka[BotRepository]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        lang = await self._get_lang(event, user, repository)

        data['i18n'] = hub.get_translator_by_locale(lang or user.language_code)
        return await handler(event, data)

    @staticmethod
    async def _get_lang(event: TelegramObject, user: User, repository: BotRepository) -> str:
        if event.callback_query and Language.WIDGET_KEY in event.callback_query.data:
            return event.callback_query.data.split(':')[1]

        if not await repository.exists(Language.REDIS_KEY.format(user.id)):
            if user.language_code in Language:
                await repository.set(Language.REDIS_KEY.format(user.id), user.language_code)
                return user.language_code
            else:
                await repository.set(Language.REDIS_KEY.format(user.id), Language.EN)
                return Language.RU

        return await repository.get(Language.REDIS_KEY.format(user.id))