from pydantic import BaseModel


class Comment(BaseModel):
    content: str

class RequestComment(Comment):
    task_slug: str

class UpdateComment(RequestComment):
    comment_id: int

class ResponseCreateComment(BaseModel):
    comment_id: str

class ResponseComment(Comment, ResponseCreateComment):
    pass
