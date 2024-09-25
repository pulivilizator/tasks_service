from aiohttp import ClientSession

from core.config.config import ConfigModel
from core import dto
from core.enums import V1TasksUrls
from core.dto.user import UserCredentials


class TodoService:
    def __init__(self,
                 session: ClientSession,
                 config: ConfigModel,
                 headers: UserCredentials):
        self._session = session
        self._config = config
        self._headers = headers

    async def get_list(self) -> list[dto.Todo]:
        url = f"{self._config.todo_backend_url}{V1TasksUrls.GET_TASKS}"
        async with self._session.get(url=url, headers=self._headers.model_dump(by_alias=True)) as response:
            todos = await response.json()
            todo_list = [dto.Todo.model_validate(todo, from_attributes=True)
                         for todo in todos]
            return todo_list

    async def get_by_slug(self, slug: str) -> dto.TodoDetail:
        url = f"{self._config.todo_backend_url}{V1TasksUrls.CURRENT_TASK.format(slug)}"
        async with self._session.get(url=url, headers=self._headers.model_dump(by_alias=True)) as response:
            todo = await response.json()
            return dto.TodoDetail.model_validate(todo, from_attributes=True)

    async def update_by_slug(self, slug: str, new_data: dict):
        url = f"{self._config.todo_backend_url}{V1TasksUrls.CURRENT_TASK.format(slug)}"
        async with self._session.patch(url=url, headers=self._headers.model_dump(by_alias=True), json=new_data) as response:
            todo = await response.json()
            return dto.TodoDetail.model_validate(todo, from_attributes=True)

    async def delete_by_slug(self, slug: str):
        url = f"{self._config.todo_backend_url}{V1TasksUrls.CURRENT_TASK.format(slug)}"
        async with self._session.delete(url=url, headers=self._headers.model_dump(by_alias=True)) as response:
            return response.status == 204