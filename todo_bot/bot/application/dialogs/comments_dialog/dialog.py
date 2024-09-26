from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, StubScroll, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from application.states import CommentsSG
from .getters import comments_getter, create_comment_getter, edit_comment_getter
from application.utils.kbd import get_scroll_buttons
from ..edit_todo_dialog.handlers import incorrect_input
from .handlers import create_comment, comment_delete, edit_comment

dialog = Dialog(
    Window(
        Format('{content}'),
        StubScroll(id='comments_scroll', pages='comments_count'),
        get_scroll_buttons('comments_scroll'),
        SwitchTo(text=Format('{create_comment}'), state=CommentsSG.comment_create, id='create_comment'),
        SwitchTo(Format('{edit_comment}'), id='edit_comment', state=CommentsSG.comment_edit, when='{edit_show}'),
        Button(Format('{delete_comment}'), id='delete_comment', on_click=comment_delete, when='{edit_show}'),
        Cancel(text=Format('{back_message}')),
        getter=comments_getter,
        state=CommentsSG.comments_list
    ),
    Window(
        Format('{create_comment_message}'),
        TextInput(
            id='comment_input',
            on_success=create_comment,
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input,
        ),
        getter=create_comment_getter,
        state=CommentsSG.comment_create
    ),
        Window(
        Format('{edit_comment_message}'),
        TextInput(
            id='comment_edit',
            on_success=edit_comment,
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input,
        ),
        getter=edit_comment_getter,
        state=CommentsSG.comment_edit
    ),

)