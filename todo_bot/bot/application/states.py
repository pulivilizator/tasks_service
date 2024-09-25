from aiogram.fsm.state import StatesGroup, State

class StartMenuSG(StatesGroup):
    menu = State()

class TodoSG(StatesGroup):
    todo_list = State()
    todo_create = State()
    todo_detail = State()