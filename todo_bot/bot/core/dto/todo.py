from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Tag(BaseModel):
    slug: str
    name: str
    created_at: datetime

class Todo(BaseModel):
    slug: str
    title: str
    created_at: datetime

class TodoDetail(Todo):
    id: str
    description: str
    end_time: datetime | None
    is_done: bool
    user: int
    tags: list[Optional[Tag]]