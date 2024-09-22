from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from core.enums import Language
from repository.implementations.bot_repository import BotRepository

@inject
async def change_lang_handler(callback: CallbackQuery,
                              widget: ManagedRadio,
                              dialog_manager: DialogManager,
                              item_id: str,
                              repository: FromDishka[BotRepository],
                              *args, **kwargs):
    await repository.set(Language.REDIS_KEY.format(callback.from_user.id), item_id)