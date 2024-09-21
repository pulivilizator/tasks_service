from dishka import make_async_container

from .providers import get_providers


def make_dishka_container():
    return make_async_container(
        *get_providers()
    )