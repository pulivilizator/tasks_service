from django.conf import settings
from redis import Redis


def registration_publish(user_id: int, password_hash: str):
    r = Redis.from_url(f'redis://{settings.config.redis.host}:{settings.config.redis.port}/{settings.config.redis.pub_db}')
    r.rpush('tg_registration', f'{user_id}:{password_hash}')