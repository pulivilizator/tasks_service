from pydantic import BaseModel


class CreateComment(BaseModel):
    content: str
    task_slug: str

class Comment(BaseModel):
    content: str
    comment_id: int

class UpdateComment(Comment, CreateComment):
    pass