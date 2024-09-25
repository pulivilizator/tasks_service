from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, ListGroup, Button, ScrollingGroup, Select, Column, SwitchTo
from aiogram_dialog.widgets.text import Format

from application.states import TodoSG
from core.enums import ElementsPerPage
from .getters import todo_getter, todo_list_getter, detail_getter
from .handlers import change_status, clear_data, delete_todo
from ...utils.kbd import get_scroll_buttons

dialog = Dialog(
    Window(
        Format('{todo_list_message}'),
        ScrollingGroup(
            ListGroup(
                SwitchTo(
                    Format("{item.title} ({item.created_at.day}.{item.created_at.month})"),
                    id="note",
                    state=TodoSG.todo_detail
                ),
                id="select_todo",
                item_id_getter=lambda item: item.slug,
                items="notes",
            ),
            height=ElementsPerPage.COUNT,
            hide_pager=True,
            id='todo_scroll',
        ),
        get_scroll_buttons('todo_scroll'),
        Cancel(text=Format('{back_message}')),
        getter=todo_list_getter,
        state=TodoSG.todo_list
    ),
    Window(
        state=TodoSG.todo_create
    ),
    Window(
        Format('{todo_message}'),
        Button(text=Format('{change_status}'), id='change_status', on_click=change_status),
        SwitchTo(text=Format('{todo_delete}'), state=TodoSG.todo_list, id="delete_todo", on_click=delete_todo),
        SwitchTo(text=Format('{back_message}'), state=TodoSG.todo_list, id="switch_todo_list", on_click=clear_data),
        getter=detail_getter,
        state=TodoSG.todo_detail
    ),
    getter=todo_getter
)