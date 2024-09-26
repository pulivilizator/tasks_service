from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.aiogram_dialog import inject
from dishka.integrations.aiogram import FromDishka

from application.states import CommentsSG
from core import dto
from core.enums import CommentUrls
from services.comment_service import CommentService


@inject
async def create_comment(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         text: str,
                         comment_service: FromDishka[CommentService]):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.start_data.get('todo'))
    new_comment = dto.CreateComment(content=text, task_slug=todo.slug)
    comment = await comment_service.create(url=CommentUrls.UPDATE_CREATE,
                                           create_data=new_comment,
                                           response_model=dto.Comment)
    dialog_manager.dialog_data['comments'].append(comment.model_dump_json())
    await dialog_manager.switch_to(state=CommentsSG.comments_list,)

@inject
async def edit_comment(message: Message,
                         widget: ManagedTextInput,
                         dialog_manager: DialogManager,
                         text: str,
                         comment_service: FromDishka[CommentService]):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.start_data.get('todo'))
    current_comment = dto.Comment.model_validate_json(dialog_manager.dialog_data.pop('current_comment'))
    new_comment = dto.UpdateComment(content=text, task_slug=todo.slug, comment_id=current_comment.comment_id)

    comment = await comment_service.update_by_slug(url=CommentUrls.UPDATE_CREATE,
                                                   new_data=new_comment,
                                                   response_model=dto.Comment)
    dialog_manager.dialog_data['comments'][dialog_manager.dialog_data['comments'].index(current_comment.model_dump_json())] = comment.model_dump_json()
    await dialog_manager.switch_to(state=CommentsSG.comments_list,)


@inject
async def comment_delete(callback: CallbackQuery,
                         widget: Button,
                         dialog_manager: DialogManager,
                         comment_service: FromDishka[CommentService],
                         *args, **kwargs):
    todo = dto.TodoDetail.model_validate_json(dialog_manager.start_data.get('todo'))
    current_comment = dto.Comment.model_validate_json(dialog_manager.dialog_data.pop('current_comment'))
    await comment_service.delete_by_slug(url=CommentUrls.DELETE.format(task_slug=todo.slug, comment_id=current_comment.comment_id))
    dialog_manager.dialog_data['comments'].remove(current_comment.model_dump_json())
    await dialog_manager.switch_to(state=CommentsSG.comments_list, )
