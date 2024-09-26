from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from core import dto
from services.todo_service import TodoService

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def edit_todo_save(callback: CallbackQuery,
                        widget: Button,
                        dialog_manager: DialogManager,
                        *args, **kwargs):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.start_data.get('todo'))
    result_data = dialog_manager.middleware_data.get('aiogd_context').widget_data
    for k, v in result_data.items():
        if hasattr(todo, k):
            if k == 'tags':
                v = [dto.Tag(name=i.strip()) for i in v.split(',')]
            if k == 'end_time':
                v = datetime.strptime(v, '%d.%m.%Y %H:%M').isoformat()
            setattr(todo, k, v)
    await dialog_manager.done(result={'todo': todo}, show_mode=ShowMode.AUTO)


async def auto_next_window(message: Message,
                           widget: ManagedTextInput,
                           dialog_manager: DialogManager,
                           text: str):
    await dialog_manager.next()

async def incorrect_input(message: Message,
                          widget: MessageInput,
                          dialog_manager: DialogManager):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(i18n.incorrect_message())

async def end_time_error(message: Message,
                         widget: ManagedTextInput | MessageInput,
                         dialog_manager: DialogManager,
                         err: Exception | None = None):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await message.answer(text=i18n.input_end_time_error())