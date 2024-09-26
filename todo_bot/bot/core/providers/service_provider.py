from aiohttp import ClientSession
from dishka import Provider, provide, Scope

from core.config.config import ConfigModel
from core.dto.user import UserCredentials
from services.comment_service import CommentService
from services.register_service import RegisterService
from services.todo_service import TodoService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_todo_service(self,
                               session: ClientSession,
                               config: ConfigModel,
                               credentials: UserCredentials) -> TodoService:
        return TodoService(session=session, headers=credentials, base_url=config.todo_backend_url)

    @provide(scope=Scope.REQUEST)
    async def get_comment_service(self,
                                  session: ClientSession,
                                  config: ConfigModel,
                                  credentials: UserCredentials) -> CommentService:
        return CommentService(session=session, headers=credentials, base_url=config.comments_backend_url)

    @provide(scope=Scope.REQUEST)
    async def get_register_service(self,
                                  session: ClientSession,
                                  config: ConfigModel,
                                  credentials: UserCredentials) -> RegisterService:
        return RegisterService(session=session, headers=credentials, config=config)