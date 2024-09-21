from dishka import Provider

from .base_provider import BaseProvider

def get_providers() -> list[Provider]:
    return [
        BaseProvider(),
    ]