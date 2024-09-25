from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Radio, Start
from aiogram_dialog.widgets.text import Format

from core.enums import Language
from .getters import get_langs, start_menu_getter
from application.states import StartMenuSG, TodoSG, CreateSG
from .handlers import change_lang_handler
from application.utils.button_checker import SetButtonChecked

dialog = Dialog(
    Window(
        Format('{menu_start_message}'),
        Start(text=Format('{start_todo_button}'), id='start_todo', state=TodoSG.todo_list),
        Start(text=Format('{start_create_button}'), id='start_create', state=CreateSG.title),
        Row(
            Radio(
                checked_text=Format('🔘 {item[1]}'),
                unchecked_text=Format('⚪️ {item[1]}'),
                id=Language.WIDGET_KEY,
                item_id_getter=lambda x: x[0],
                on_state_changed=change_lang_handler,
                items='languages',
            ),
        ),
        getter=get_langs,
        state=StartMenuSG.menu,
    ),
    on_start=SetButtonChecked(Language),
    getter=start_menu_getter
)