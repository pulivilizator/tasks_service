from enum import StrEnum
from http import HTTPMethod


class V1TasksUrls(StrEnum):
    GET_TASKS = 'v1/tasks/'
    GET_CURRENT_TASK = 'v1/tasks/{}/'

class CommentKeys(StrEnum):
    COMMENTS_KEY = 'task:{}:comments'
    COMMENT_ID = 'task:{}:comment_id'