from aiogram import Router
from .handlers.commands_handler import router as commands_router

def get_routers() -> list[Router]:
    return [
        commands_router,
    ]