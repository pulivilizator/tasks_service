from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Next, Back, Button
from aiogram_dialog.widgets.text import Format

from application.dialogs.edit_todo_dialog.filters import filter_end_time
from application.dialogs.edit_todo_dialog.handlers import auto_next_window, incorrect_input, end_time_error
from application.states import CreateSG
from .getters import create_getter
from .handlers import create_todo_save

dialog = Dialog(
    Window(
        Format('{create_title}'),
        TextInput(
            id='title',
            on_success=auto_next_window
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Cancel(text=Format('{cancel}')),
        state=CreateSG.title
    ),
    Window(
        Format('{create_description}'),
        TextInput(
            id='description',
            on_success=auto_next_window
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Back(text=Format('{back}')),
        Cancel(text=Format('{cancel}')),
        state=CreateSG.description
    ),
    Window(
        Format('{create_end_time}'),
        TextInput(
            id='end_time',
            type_factory=filter_end_time,
            on_success=auto_next_window,
            on_error=end_time_error
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Next(text=Format('{skip}')),
        Back(text=Format('{back}')),
        Cancel(text=Format('{cancel}')),
        state=CreateSG.end_time
    ),
    Window(
        Format('{create_tags}'),
        TextInput(
            id='tags',
            on_success=auto_next_window
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Next(text=Format('{skip}')),
        Back(text=Format('{back}')),
        Cancel(text=Format('{cancel}')),
        state=CreateSG.tags
    ),
    Window(
        Format('{confirm}'),
        Button(text=Format('{done}'), id='edit_done', on_click=create_todo_save),
        Cancel(text=Format('{cancel}')),
        state=CreateSG.save
    ),
    getter=create_getter
)