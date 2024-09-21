from datetime import timedelta
from typing import Optional

from redis.asyncio import Redis

from .base import AbstractNoSQLRepository


class RedisRepository(AbstractNoSQLRepository):
    def __init__(self, r: Redis):
        self.r = r

    async def set(self, name, value):
        await self.r.set(name, value)

    async def get(self, name):
        result = await self.r.get(name)
        return result.decode('utf-8') if result else None

    async def set_ex(self, name: bytes | str,
                     value: bytes | str | int | float,
                     time: int | timedelta):
        await self.r.setex(name=name, value=value, time=time)

    async def get_ex(self, name: str,
                     ex: Optional[int] = None,
                     px: Optional[int] = None,
                     persist: Optional[bool] = False):
        result = await self.r.getex(name=name, ex=ex, px=px, persist=persist)
        return result.decode('utf-8') if result else None

    async def delete(self, name):
        await self.r.delete(name)

    async def exists(self, name):
        return await self.r.exists(name)