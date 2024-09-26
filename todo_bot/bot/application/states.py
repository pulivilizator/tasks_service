from aiogram.fsm.state import StatesGroup, State

class StartMenuSG(StatesGroup):
    menu = State()

class TodoSG(StatesGroup):
    todo_list = State()
    todo_create = State()
    todo_detail = State()

class EditSG(StatesGroup):
    title = State()
    description = State()
    end_time = State()
    tags = State()
    save = State()

class CreateSG(StatesGroup):
    title = State()
    description = State()
    end_time = State()
    tags = State()
    save = State()

class CommentsSG(StatesGroup):
    comments_list = State()
    comment_create = State()
    comment_edit = State()