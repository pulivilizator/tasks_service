from dishka import Provider

from .auth_provider import AuthProvider
from .base_provider import BaseProvider
from .repository_providers import RepositoryProvider
from .service_provider import ServiceProvider


def get_providers() -> list[Provider]:
    return [
        BaseProvider(),
        RepositoryProvider(),
        AuthProvider(),
        ServiceProvider(),
    ]