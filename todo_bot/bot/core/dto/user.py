from pydantic import BaseModel, Field


class UserCredentials(BaseModel):
    public_key: str = Field(alias='X-Public-Key')
    user_id: str = Field(alias='X-Tg-Id')

class RegisterUser(BaseModel):
    tg_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None