from pydantic import BaseModel, RedisDsn

class RedisConfig(BaseModel):
    dsn: RedisDsn
    pubsub_dsn: RedisDsn

class BotConfig(BaseModel):
    token: str