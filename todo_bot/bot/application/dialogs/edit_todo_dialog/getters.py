from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

async def edit_getter(dialog_manager: DialogManager,
                      i18n: TranslatorRunner,
                      **kwargs):

    return {
        'confirm': i18n.edit.confirm(),
        'skip': i18n.edit.skip(),
        'back': i18n.edit.back(),
        'cancel': i18n.edit.cancel(),
        'done': i18n.edit.save(),
        'new_title': i18n.edit.new_title(),
        'new_description': i18n.edit.new_description(),
        'new_end_time': i18n.edit.new_end_time(),
        'new_tags': i18n.edit.new_tags()
    }