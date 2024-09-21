from aiohttp import ClientSession
from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from core.config.config import ConfigModel
from repository.implementations.comments_repository import CommentRepository
from services.comments_service import CommentsService


class RepositoryProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_comments_repository(self, r: Redis) -> CommentRepository:
        return CommentRepository(r=r)

class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_comments_service(self,
                             session: ClientSession,
                             repository: CommentRepository,
                             config: ConfigModel) -> CommentsService:

        return CommentsService(session=session,
                               repository=repository,
                               config=config)