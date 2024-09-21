from http import HTTPMethod
from typing import Optional

from aiohttp import ClientSession, ClientResponseError
from fastapi import HTTPException
from starlette import status
from starlette.authentication import AuthenticationError

from core import dto
from core.config.config import ConfigModel
from core.enums import V1TasksUrls
from repository.implementations.comments_repository import CommentRepository
from services.exceptions import TaskNotFound, TooManyRequestsError


class CommentsService:
    def __init__(self, session: ClientSession, repository: CommentRepository, config: ConfigModel):
        self.repository = repository
        self.session = session
        self.config = config

    async def get_comments(self, task_slug: str) -> list[dto.ResponseComment]:
        comments = await self.repository.get_comments(task_slug)
        return comments

    async def create_comment(self, comment: dto.RequestComment) -> dto.ResponseCreateComment:
        comment_id = await self.repository.save_comment(comment)
        return comment_id

    async def update_comment(self, new_comment: dto.UpdateComment) -> bool:
        return await self.repository.update_comment(new_comment)

    async def delete_comment(self, task_slug: str, comment_id: str) -> bool:
        return await self.repository.delete_comment(task_slug=task_slug, comment_id=comment_id)

    async def check_task_auth(self, headers: dict, cookies: dict, task_slug: Optional[str] = None):
        """
        Проверяет аутентификацию или существование задачи(что включает в себя аутентификацию)
        """
        print(task_slug)
        path = V1TasksUrls.GET_CURRENT_TASK.format(task_slug) if task_slug else V1TasksUrls.GET_TASKS
        try:
            await self._make_request(method=HTTPMethod.GET,
                                     url=self.config.backend_url.unicode_string() + path,
                                     headers=headers,
                                     cookies=cookies)
        except ClientResponseError as e:
            if e.status == status.HTTP_404_NOT_FOUND:
                raise TaskNotFound(task_slug)
            if e.status in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            if e.status == status.HTTP_429_TOO_MANY_REQUESTS:
                raise TooManyRequestsError()
            raise HTTPException(status_code=e.status, detail=e.message, headers=e.headers)



    async def _make_request(self,
                            method: HTTPMethod,
                            url: str,
                            headers: Optional[dict] = None,
                            json: Optional[dict] = None,
                            cookies: Optional[dict] = None):
        async with self.session.request(method, url, json=json, cookies=cookies, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

