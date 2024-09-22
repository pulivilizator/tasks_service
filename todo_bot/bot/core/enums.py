from enum import StrEnum

class BaseKeys(StrEnum):
    WIDGET_KEY: str
    REDIS_KEY: str

class Language(BaseKeys):
    RU = 'ru'
    EN = 'en'

    WIDGET_KEY = 'language'
    REDIS_KEY = 'language:{}'
