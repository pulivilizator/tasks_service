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

class CommentUrls(StrEnum):
    UPDATE_CREATE = 'comments/'
    GET = 'comments/{}/'
    DELETE = 'comments/{task_slug}/{comment_id}/'

class AuthUrls(StrEnum):
    REGISTER = 'v1/auth/registration/'

class ElementsPerPage(IntEnum):
    COUNT = 6

class HttpRegisterConfirmation(StrEnum):
    YES = 'http_register_yes'
    NO = 'http_register_no'
    HASH_KEY = '{}:HASH'