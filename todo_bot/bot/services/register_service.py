from aiohttp import ClientSession

from core import dto
from core.config.config import ConfigModel
from core.enums import AuthUrls


class RegisterService:
    def __init__(self,
                 config: ConfigModel,
                 session: ClientSession,
                 headers: dto.UserCredentials):
        self._config = config
        self._session = session
        self._headers = headers

    async def register_user(self, user_data: dto.RegisterUser):
        url = f'{self._config.todo_backend_url}{AuthUrls.REGISTER}'
        async with self._session.post(url=url,
                                      headers=self._headers.model_dump(by_alias=True),
                                      json=user_data.model_dump(mode='json')) as response:
            return response.status

    async def http_register_user(self, tg_id: int, password: str):
        url = f'{self._config.todo_backend_url}{AuthUrls.REGISTER}'
        async with self._session.post(url=url,
                                      headers=self._headers.model_dump(by_alias=True),
                                      json={'tg_id': tg_id, 'password': password, 'confirmation': True}) as response:
            return response.status