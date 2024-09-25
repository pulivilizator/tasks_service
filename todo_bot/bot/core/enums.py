from enum import StrEnum, IntEnum


class BaseKeys(StrEnum):
    WIDGET_KEY: str
    REDIS_KEY: str

class Language(BaseKeys):
    RU = 'ru'
    EN = 'en'

    WIDGET_KEY = 'language'
    REDIS_KEY = 'language:{}'

class V1TasksUrls(StrEnum):
    TASKS = 'v1/tasks/'
    CURRENT_TASK = 'v1/tasks/{}/'

class ElementsPerPage(IntEnum):
    COUNT = 6