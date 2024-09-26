from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

async def create_getter(dialog_manager: DialogManager,
                      i18n: TranslatorRunner,
                      **kwargs):

    return {
        'confirm': i18n.create.confirm(),
        'skip': i18n.edit.skip(),
        'back': i18n.edit.back(),
        'cancel': i18n.edit.cancel(),
        'done': i18n.edit.save(),
        'create_title': i18n.create.title(),
        'create_description': i18n.create.description(),
        'create_end_time': i18n.create.end_time(),
        'create_tags': i18n.create.tags()
    }