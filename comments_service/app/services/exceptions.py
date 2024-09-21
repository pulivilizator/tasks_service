class TaskNotFound(Exception):
    def __init__(self, task_slug):
        msg = f'Task {task_slug} not found'
        super().__init__(msg)

class TooManyRequestsError(Exception):
    def __init__(self):
        msg = f'Too many requests. Retry later'
        super().__init__(msg)