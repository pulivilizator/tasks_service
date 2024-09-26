from typing import TYPE_CHECKING, Optional

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from core import dto
from core.enums import CommentUrls
from services.comment_service import CommentService

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner

@inject
async def comments_getter(dialog_manager: DialogManager,
                          i18n: TranslatorRunner,
                          comment_service: FromDishka[CommentService],
                          **kwargs):
    scroll: ManagedScroll = dialog_manager.find('comments_scroll')

    comments = dialog_manager.dialog_data.get('comments')
    todo = dto.TodoDetail.model_validate_json(dialog_manager.start_data.get('todo'))

    if comments is None:
        comments = await comment_service.get_list(url=CommentUrls.GET.format(todo.slug), response_model=dto.Comment)
        json_comments = [comment.model_dump_json() for comment in comments]
        dialog_manager.dialog_data.update({'comments': json_comments})
    else:
        comments = [dto.Comment.model_validate_json(comment) for comment in comments]

    current_comment: Optional[dto.Comment] = None
    if comments:

        comment_number = await scroll.get_page()
        if comment_number >= len(comments):
            comment_number = len(comments) - 1
        current_comment = comments[comment_number]
        dialog_manager.dialog_data.update({'current_comment': current_comment.model_dump_json()})

    return {
        'comments_count': len(comments),
        'content': current_comment.content if current_comment else i18n.comments_empty(),
        'back_message': i18n.back.button(),
        'single_page': len(comments) > 1,
        'create_comment': i18n.comment.create.button(),
        'delete_comment': i18n.comment.delete.button(),
        'edit_comment': i18n.comment.edit.button(),
        'edit_show': current_comment is not None
    }

async def create_comment_getter(dialog_manager: DialogManager,
                                i18n: TranslatorRunner,
                                **kwargs):
    return {
        'create_comment_message': i18n.comment.create.message(),
    }

async def edit_comment_getter(dialog_manager: DialogManager,
                              i18n: TranslatorRunner,
                              **kwargs):
    return {
        'edit_comment_message': i18n.comment.edit.message(),
    }
