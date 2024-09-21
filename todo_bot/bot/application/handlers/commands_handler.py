from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

router = Router()

@router.message(CommandStart())
async def start_process(message: Message,
                        dialog_manager: DialogManager):
    pass