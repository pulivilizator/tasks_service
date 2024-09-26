from datetime import datetime
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from application.states import TodoSG
from core import dto
from core.config.config import ConfigModel
from core.enums import V1TasksUrls
from services.todo_service import TodoService

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def create_todo_save(callback: CallbackQuery,
                           widget: Button,
                           dialog_manager: DialogManager,
                           todo_service: FromDishka[TodoService],
                           *args, **kwargs):
    result_data = dialog_manager.middleware_data.get('aiogd_context').widget_data
    if result_data.get('tags'):
        result_data['tags'] = [dto.Tag(name=i.strip()) for i in result_data['tags'].split(',')]
    if result_data.get('end_time'):
        result_data['end_time'] = datetime.strptime(result_data['end_time'], '%d.%m.%Y %H:%M').isoformat()
    new_todo = dto.CreateTodo.model_validate(result_data, from_attributes=True)
    todo = await todo_service.create(url=V1TasksUrls.TASKS,
                                     create_data=new_todo,
                                     response_model=dto.TodoDetail)
    await dialog_manager.done(show_mode=ShowMode.AUTO)