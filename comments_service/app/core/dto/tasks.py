from pydantic import BaseModel


class Task(BaseModel):
    id: str
    slug: str
    title: str
    description: str | None = None
