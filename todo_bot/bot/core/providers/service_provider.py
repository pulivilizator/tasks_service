from aiohttp import ClientSession
from dishka import Provider, provide, Scope

from core.config.config import ConfigModel
from core.dto.user import UserCredentials
from services.todo_service import TodoService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_todo_service(self,
                               session: ClientSession,
                               config: ConfigModel,
                               credentials: UserCredentials) -> TodoService:
        return TodoService(session=session, config=config, headers=credentials)