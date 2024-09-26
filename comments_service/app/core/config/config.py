from environs import Env
from pydantic import BaseModel, HttpUrl

from core.config.models import RedisConfig


class ConfigModel(BaseModel):
    redis: RedisConfig
    backend_url: HttpUrl

def get_config(path: str = None) -> ConfigModel:
    env = Env()
    env.read_env(path)

    return ConfigModel(
        redis=RedisConfig(
            dsn='redis://' + env.str('REDIS_DSN')
        ),

        backend_url=env.str('TASKS_BACKEND_URL')
    )