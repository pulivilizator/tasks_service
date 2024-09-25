from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    public_key: str = Field(alias='X-Public-Key')
    user_id: str = Field(alias='X-Tg-Id')
