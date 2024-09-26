from datetime import datetime
from typing import TYPE_CHECKING, Dict, List

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from dishka.integrations.aiogram import FromDishka

from core import dto
from core.enums import ElementsPerPage, V1TasksUrls
from services.todo_service import TodoService

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


@inject
async def todo_list_getter(dialog_manager: DialogManager,
                           i18n: TranslatorRunner,
                           todo_service: FromDishka[TodoService],
                           **kwargs):
    todos = dialog_manager.dialog_data.get('todos')
    if todos is None:
        todo_list: list[dto.Todo] = await todo_service.get_list(url=V1TasksUrls.TASKS, response_model=dto.Todo)
        dialog_manager.dialog_data.update({'todos': [todo.model_dump_json() for todo in todo_list]})
    else:
        todo_list = [dto.Todo.model_validate_json(todo)
                     for todo in todos]

    return {
        'todo_list_message': i18n.todo.list.message(),
        'todos': todo_list,
        'single_page': len(todo_list) / ElementsPerPage.COUNT > 1
    }

async def todo_getter(dialog_manager: DialogManager,
                      i18n: TranslatorRunner,
                      **kwargs) -> dict[str, tuple | str]:

    return {
        'back_message': i18n.back.button()
    }

@inject
async def detail_getter(dialog_manager: DialogManager,
                        i18n: TranslatorRunner,
                        todo_service: FromDishka[TodoService],
                        **kwargs):
    todo_slug = dialog_manager.dialog_data.get('todo_slug')
    if todo_slug is None:
        todo_slug = dialog_manager.event.data.split(':')[1]
        todo = await todo_service.get_by_slug(url=V1TasksUrls.CURRENT_TASK.format(todo_slug), response_model=dto.TodoDetail)
        dialog_manager.dialog_data.update({'todo_slug': todo_slug})
        dialog_manager.dialog_data.update({'todo': todo.model_dump_json()})
    else:
        todo = dto.TodoDetail.model_validate_json(dialog_manager.dialog_data.get('todo'))

    end_time = i18n.todo.end_time.default()
    if todo.end_time is not None:
        end_time = todo.end_time.strftime('%d.%m.%Y %H:%M')


    is_done = i18n.todo.done() if todo.is_done else i18n.todo.not_done()
    tags = ' | '.join(['#' + tag.name for tag in todo.tags]) if todo.tags else ''
    return {
        'todo_message': i18n.todo.message(title=todo.title,
                                          description=todo.description,
                                          created=todo.created_at.strftime('%d.%m.%Y %H:%M'),
                                          end_time=end_time,
                                          is_done=is_done,
                                          tags=tags
                                          ),
        'change_status': i18n.todo.change_status(),
        'todo_delete': i18n.todo.delete_button(),
        'start_edit': i18n.todo.edit_button(),
        'show_comments': i18n.todo.show_comments_button(),
    }