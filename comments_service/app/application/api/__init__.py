from fastapi import APIRouter

from .comments import router as comments_router


def get_routers() -> list[APIRouter]:
    return [
        comments_router
    ]