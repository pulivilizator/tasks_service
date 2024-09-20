from environs import Env
from dataclasses import dataclass


@dataclass
class Database:
    db: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class Django:
    secret_key: str
    debug: bool
    allowed_hosts: list


@dataclass
class Celery:
    celery_broker_url: str
    celery_result_backend: str


@dataclass
class Config:
    database: Database
    django: Django
    celery: Celery


def get_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        database=Database(
            db=env('DB_NAME'),
            host=env('DB_HOST'),
            port=env.int('DB_PORT'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD'),
        ),
        django=Django(
            secret_key=env('DJANGO_SECRET_KEY'),
            allowed_hosts=env.list('ALLOWED_HOSTS', delimiter=' '),
            debug=env.bool('DEBUG_MODE', default=False),
        ),
        celery=Celery(
            celery_broker_url=f'redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/{env('CELERY_REDIS_BROKER_DB')}',
            celery_result_backend=f'redis://{env('REDIS_HOST')}{env('REDIS_PORT')}/{env('CELERY_REDIS_RESULT_DB')}',
        ),
    )