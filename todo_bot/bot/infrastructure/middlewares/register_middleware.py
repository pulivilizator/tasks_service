from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from dishka.integrations.aiogram import FromDishka
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core import dto
from core.enums import Language
from repository.implementations.bot_repository import BotRepository
from services.register_service import RegisterService
from .inject_middleware import aiogram_middleware_inject


class RegisterMiddleware(BaseMiddleware):
    @aiogram_middleware_inject
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
            repository: FromDishka[BotRepository],
            service: FromDishka[RegisterService],
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        if not await repository.exists(Language.REDIS_KEY.format(user.id)):
            user_data = dto.RegisterUser(tg_id=user.id,
                                         username=user.username,
                                         first_name=user.first_name,
                                         last_name=user.last_name)
            await service.register_user(user_data=user_data)

        return await handler(event, data)