from fastapi import HTTPException
from starlette import status


class TaskNotFound(HTTPException):
    def __init__(self, task_slug):
        msg = f'Task {task_slug} not found'
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail=msg)

class TooManyRequestsError(HTTPException):
    def __init__(self):
        msg = f'Too many requests. Retry later'
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                         detail=msg)