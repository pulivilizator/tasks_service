from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject
from dishka import FromDishka
from fluentogram import TranslatorRunner

from core.enums import Language

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def start_menu_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           **kwargs) -> dict[str, tuple | str]:
    return {
        'start_menu_message': i18n.start_menu_message(),
    }

@inject
async def get_langs(dialog_manager: DialogManager,
                    i18n: TranslatorRunner,
                    **kwargs) -> dict[str, tuple | str]:
    return {
        'languages': (
            (Language.RU, i18n.lang.ru()),
            (Language.EN, i18n.lang.en())
        )
    }