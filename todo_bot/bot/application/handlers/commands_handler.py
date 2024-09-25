from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from dishka.integrations.aiogram import FromDishka

from application.states import StartMenuSG
from core import dto
from services.todo_service import TodoService

router = Router()

@router.message(CommandStart())
async def start_process(message: Message,
                        dialog_manager: DialogManager,
                        serv: FromDishka[TodoService]):
    await dialog_manager.start(state=StartMenuSG.menu, mode=StartMode.RESET_STACK)