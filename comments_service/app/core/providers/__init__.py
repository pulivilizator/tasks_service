from dishka import Provider

from .base_provider import BaseProvider
from .services_provider import RepositoryProvider, ServicesProvider


def get_providers() -> list[Provider]:
    return [
        BaseProvider(),
        RepositoryProvider(),
        ServicesProvider(),
    ]