from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Cancel, Back, Button

from aiogram_dialog.widgets.text import Format

from .filters import filter_end_time
from .getters import edit_getter
from application.states import EditSG
from .handlers import edit_todo_save, auto_next_window, incorrect_input, end_time_error

dialog = Dialog(
    Window(
        Format('{new_title}'),
        TextInput(
            id='title',
            on_success=auto_next_window
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Next(text=Format('{skip}')),
        Cancel(text=Format('{cancel}')),
        state=EditSG.title
    ),
    Window(
        Format('{new_description}'),
        TextInput(
            id='description',
            on_success=auto_next_window
        ),
        MessageInput(
            content_types=ContentType.ANY,
            func=incorrect_input
        ),
        Next(text=Format('{skip}')),
        Back(text=Format('{back}')),
        Cancel(text=Format('{cancel}')),
        state=EditSG.description
    ),
    Window(
        Format('{new_end_time}'),
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
        state=EditSG.end_time
    ),
    Window(
        Format('{new_tags}'),
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
        state=EditSG.tags
    ),
    Window(
        Format('{confirm}'),
        Button(text=Format('{done}'), id='edit_done', on_click=edit_todo_save),
        Cancel(text=Format('{cancel}')),
        state=EditSG.save
    ),
    getter=edit_getter
)