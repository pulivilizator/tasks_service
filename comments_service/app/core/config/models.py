from pydantic import BaseModel, RedisDsn

class RedisConfig(BaseModel):
    dsn: RedisDsn