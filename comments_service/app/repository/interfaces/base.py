from abc import ABC, abstractmethod

class AbstractNoSQLRepository(ABC):
    @abstractmethod
    async def set(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError