from environs import Env
from pydantic import BaseModel, HttpUrl

from core.config.models import RedisConfig, BotConfig


class ConfigModel(BaseModel):
    redis: RedisConfig
    bot: BotConfig
    todo_backend_url: HttpUrl
    comments_backend_url: HttpUrl

def get_config(path: str = None) -> ConfigModel:
    env = Env()
    env.read_env(path)

    return ConfigModel(
        redis=RedisConfig(
            dsn=env.str('REDIS_STORAGE_DSN')
        ),
        bot=BotConfig(
            token=env.str('BOT_TOKEN')
        ),
        todo_backend_url=env.str('TODO_BACKEND_URL'),
        comments_backend_url=env.str('COMMENTS_BACKEND_URL')
    )