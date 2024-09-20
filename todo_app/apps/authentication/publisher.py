from todo_app.config import get_config
from redis import Redis


def registration_publish(user_id: int, password_hash: str):
    config = get_config()
    r = Redis.from_url(f'redis://{config.redis.host}:{config.redis.port}/{config.redis.pub_db}')
    a = r.publish('tg_registration', f'{user_id}:{password_hash}')
    print('publish', a)