from core import dto
from core.enums import CommentKeys
from repository.interfaces.redis_repository import RedisRepository


class CommentRepository(RedisRepository):
    async def save_comment(self, comment: dto.RequestComment) -> dto.ResponseCreateComment:
        comments_incr_key = CommentKeys.COMMENT_ID.format(comment.task_slug)
        comment_id = await self._r.incr(comments_incr_key)
        comments_key = CommentKeys.COMMENTS_KEY.format(comment.task_slug)
        await self._r.hset(comments_key, comment_id, comment.content)
        return dto.ResponseCreateComment(comment_id=str(comment_id))

    async def get_comments(self, task_slug: str) -> list[dto.ResponseComment]:
        comments_key = CommentKeys.COMMENTS_KEY.format(task_slug)
        comments = await self._r.hgetall(comments_key)
        decoded_comments = [dto.ResponseComment(comment_id= k.decode('utf-8'), content = v.decode('utf-8'))
                            for k, v in comments.items()]
        return decoded_comments

    async def update_comment(self, new_comment: dto.UpdateComment) -> bool:
        comments_key = CommentKeys.COMMENTS_KEY.format(new_comment.task_slug)
        if await self._r.hexists(comments_key, new_comment.comment_id):
            await self._r.hset(comments_key, new_comment.comment_id, new_comment.content)
            return True
        return False

    async def delete_comment(self, task_slug, comment_id: str) -> bool:
        comments_key = CommentKeys.COMMENTS_KEY.format(task_slug)
        result = await self._r.hdel(comments_key, comment_id)

        return result == 1