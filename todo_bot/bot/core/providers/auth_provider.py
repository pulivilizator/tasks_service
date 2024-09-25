import base64

from aiogram.types import TelegramObject
from dishka import Provider, provide, Scope, from_context

from core.config.config import ConfigModel
from core.dto.user import UserCredentials


class AuthProvider(Provider):
    obj = from_context(provides=TelegramObject, scope=Scope.REQUEST)
    @provide(scope=Scope.REQUEST)
    async def get_credentials(self, obj: TelegramObject, config: ConfigModel) -> UserCredentials:
        public_key_base64 = base64.b64encode(config.public_key.read_text().encode()).decode()
        return UserCredentials(**{
            'X-Public-Key': public_key_base64,
            'X-Tg-Id': str(obj.from_user.id)
        })