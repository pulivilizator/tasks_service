from typing import Any, Literal

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, Data
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from application.states import CreateSG, EditSG, CommentsSG
from core import dto
from core.enums import V1TasksUrls
from services.todo_service import TodoService


@inject
async def change_status(callback: CallbackQuery,
                        widget: Button,
                        dialog_manager: DialogManager,
                        todo_service: FromDishka[TodoService],
                        *args, **kwargs):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.dialog_data.get('todo'))

    is_done = not todo.is_done
    todo.is_done = is_done
    dialog_manager.dialog_data.update({'todo': todo.model_dump_json()})
    await todo_service.update_by_slug(url=V1TasksUrls.CURRENT_TASK.format(todo.slug),
                                      new_data=dto.UpdateStatus(is_done=is_done),
                                      response_model=dto.TodoDetail)

@inject
async def delete_todo(callback: CallbackQuery,
                      widget: Button,
                      dialog_manager: DialogManager,
                      todo_service: FromDishka[TodoService],
                      *args, **kwargs):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.dialog_data.get('todo'))
    await todo_service.delete_by_slug(url=V1TasksUrls.CURRENT_TASK.format(todo.slug))
    dialog_manager.dialog_data.clear()

async def start_show_comments(callback: CallbackQuery,
                             widget: Button,
                             dialog_manager: DialogManager,
                             *args, **kwargs):
    await dialog_manager.start(state=CommentsSG.comments_list, data=dialog_manager.dialog_data)

async def start_edit(callback: CallbackQuery,
                     widget: Button,
                     dialog_manager: DialogManager,
                     *args, **kwargs):
   await dialog_manager.start(state=EditSG.title, data=dialog_manager.dialog_data)


@inject
async def send_todo(start_data: Data,
                    result: dict[Literal['todo']: dto.TodoDetail],
                    dialog_manager: DialogManager,
                    todo_service: FromDishka[TodoService]):
    if result:
        todo: dto.TodoDetail = result.get('todo')
        new_todo = await todo_service.update_by_slug(url=V1TasksUrls.CURRENT_TASK.format(todo.slug),
                                                     new_data=todo, response_model=dto.TodoDetail)
        dialog_manager.dialog_data.update({'todo': new_todo.model_dump_json()})


async def clear_data(callback: CallbackQuery,
                     widget: Button,
                     dialog_manager: DialogManager,
                     *args, **kwargs):
    dialog_manager.dialog_data.clear()