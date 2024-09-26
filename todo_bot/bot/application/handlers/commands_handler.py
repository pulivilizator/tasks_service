from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka

from application.states import StartMenuSG
from core.enums import HttpRegisterConfirmation
from repository.implementations.bot_repository import BotRepository
from services.register_service import RegisterService

router = Router()

@router.message(CommandStart())
async def start_process(message: Message,
                        dialog_manager: DialogManager,):
    await dialog_manager.start(state=StartMenuSG.menu, mode=StartMode.RESET_STACK)

@router.callback_query(F.data.startswith(HttpRegisterConfirmation.YES))
async def http_registration(cb: CallbackQuery,
                            repository: FromDishka[BotRepository],
                            service: FromDishka[RegisterService]):
    pass_hash = await repository.get(HttpRegisterConfirmation.HASH_KEY.format(cb.from_user.id))

    await service.http_register_user(cb.from_user.id, pass_hash)
