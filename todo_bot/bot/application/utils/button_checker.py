import asyncio
from typing import Callable, Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.enums import BaseKeys
from repository.implementations.bot_repository import BotRepository


class SetButtonChecked:
    def __init__(self, *keys: BaseKeys):
        self._keys = keys

    @inject
    async def __call__(self, _: Any, dialog_manager: DialogManager, repository: FromDishka[BotRepository]):
        await self._set_default_buttons(_, dialog_manager=dialog_manager, keys=self._keys, repository=repository)

    async def _set_checked(self, repository: BotRepository, dialog_manager: DialogManager, key: BaseKeys):
        user = dialog_manager.event.from_user
        user_value = await repository.get(key.REDIS_KEY.format(user.id))
        widget: ManagedWidget = dialog_manager.find(key.WIDGET_KEY)
        await widget.set_checked(user_value)

    async def _set_default_buttons(self, _, dialog_manager: DialogManager, keys, repository: BotRepository):
        await asyncio.gather(
            *[
                asyncio.create_task(self._set_checked(repository, dialog_manager, cache_key))
                for cache_key in keys
            ]
        )
