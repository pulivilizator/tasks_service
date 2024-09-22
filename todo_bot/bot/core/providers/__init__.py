from dishka import Provider

from .base_provider import BaseProvider
from .repository_providers import RepositoryProvider


def get_providers() -> list[Provider]:
    return [
        BaseProvider(),
        RepositoryProvider(),
    ]