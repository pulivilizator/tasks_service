from datetime import timedelta
from typing import Optional

from redis.asyncio import Redis

from .base import AbstractNoSQLRepository


class RedisRepository(AbstractNoSQLRepository):
    def __init__(self, r: Redis):
        self._r = r

    async def set(self, name, value):
        await self._r.set(name, value)

    async def get(self, name):
        result = await self._r.get(name)
        return result.decode('utf-8') if result else None

    async def set_ex(self, name: bytes | str,
                     value: bytes | str | int | float,
                     time: int | timedelta):
        await self._r.setex(name=name, value=value, time=time)

    async def get_ex(self, name: str,
                     ex: Optional[int] = None,
                     px: Optional[int] = None,
                     persist: Optional[bool] = False):
        result = await self._r.getex(name=name, ex=ex, px=px, persist=persist)
        return result.decode('utf-8') if result else None

    async def delete(self, name):
        await self._r.delete(name)

    async def exists(self, name):
        return await self._r.exists(name)