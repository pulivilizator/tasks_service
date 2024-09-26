from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Tag(BaseModel):
    slug: str | None = None
    name: str
    created_at: datetime | None = None

class Todo(BaseModel):
    slug: str
    title: str
    created_at: datetime

class TodoDetail(Todo):
    id: str
    description: str | None = None
    end_time: datetime |None = None
    is_done: bool = False
    user: int
    tags: list[Optional[Tag]]


class CreateTodo(BaseModel):
    title: str
    description: str | None = None
    end_time: datetime | None = None
    tags: list[Optional[Tag]] = []

class UpdateStatus(BaseModel):
    is_done: bool