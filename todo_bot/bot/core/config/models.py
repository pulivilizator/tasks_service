from pydantic import BaseModel, RedisDsn

class RedisConfig(BaseModel):
    dsn: RedisDsn

class BotConfig(BaseModel):
    token: str