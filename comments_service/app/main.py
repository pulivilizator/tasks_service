from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from application.api import get_routers
from core.dishka_container import make_dishka_container


def main():
    app = FastAPI(title='Comments service',
                  version='1.0.0',
                  summary='Сервис по обработке комментариев к задачам')

    [app.include_router(router) for router in get_routers()]

    container = make_dishka_container()

    setup_dishka(app=app, container=container)

    return app