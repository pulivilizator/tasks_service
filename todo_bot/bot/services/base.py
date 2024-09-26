from abc import ABC, abstractmethod
from typing import Any, TypeVar, Type

from aiohttp import ClientSession
from pydantic import BaseModel

from core.config.config import ConfigModel
from core.dto import UserCredentials

ResponseModel = TypeVar('ResponseModel', bound=BaseModel)

class AbstractService(ABC):

    @abstractmethod
    async def get_by_slug(self, surl: str, response_model: ResponseModel) -> ResponseModel:
        raise NotImplementedError

    @abstractmethod
    async def update_by_slug(self, url: str, new_data: BaseModel, response_model: ResponseModel) -> ResponseModel:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_slug(self, url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self,url: str, data: BaseModel, response_model: ResponseModel) -> ResponseModel:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, url: str, response_model: ResponseModel) -> list[ResponseModel]:
        raise NotImplementedError


class BaseService(AbstractService):
    def __init__(self,
                 session: ClientSession,
                 headers: UserCredentials,
                 base_url: str):
        self._session = session
        self._headers = headers
        self._base_url = base_url

    async def get_by_slug(self, url: str, response_model: Type[ResponseModel]) -> ResponseModel:
        url = f'{self._base_url}{url}'
        async with self._session.get(url,
                                     headers=self._headers.model_dump(by_alias=True)) as response:
            response.raise_for_status()
            data = await response.json()
            return response_model.model_validate(data, from_attributes=True)

    async def update_by_slug(self, url: str, new_data: BaseModel, response_model: Type[ResponseModel]) -> ResponseModel:
        url = f'{self._base_url}{url}'
        async with self._session.patch(url=url,
                                       headers=self._headers.model_dump(by_alias=True),
                                       json=new_data.model_dump(mode='json')) as response:
            data = await response.json()
            return response_model.model_validate(data, from_attributes=True)

    async def delete_by_slug(self, url: str) -> bool:
        url = f'{self._base_url}{url}'
        async with self._session.delete(url=url,
                                        headers=self._headers.model_dump(by_alias=True)) as response:
            return response.status == 204

    async def create(self, url: str, create_data: BaseModel, response_model: Type[ResponseModel]) -> ResponseModel:
        url = f'{self._base_url}{url}'
        async with self._session.post(url=url,
                                      headers=self._headers.model_dump(by_alias=True),
                                      json=create_data.model_dump(mode='json')) as response:
            data = await response.json()
            return response_model.model_validate(data, from_attributes=True)

    async def get_list(self, url: str, response_model: Type[ResponseModel]) -> list[ResponseModel]:
        url = f'{self._base_url}{url}'
        async with self._session.get(url=url, headers=self._headers.model_dump(by_alias=True)) as response:
            data = await response.json()
            todo_list = [response_model.model_validate(el, from_attributes=True)
                         for el in data]
            return todo_list
