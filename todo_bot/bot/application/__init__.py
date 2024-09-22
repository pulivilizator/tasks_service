from aiogram import Router
from .handlers.commands_handler import router as commands_router
from .dialogs import start_dialog

def get_routers() -> list[Router]:
    return [
        commands_router,
        start_dialog,
    ]