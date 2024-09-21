from typing import Annotated

from fastapi import APIRouter, Path, Body, Request
from dishka.integrations.fastapi import FromDishka, inject
from fastapi.params import Depends
from starlette import status

from core import dto
from services.comments_service import CommentsService
from application.dependencies import check_auth

router = APIRouter(tags=['Comment'],
                   dependencies=[Depends(check_auth)],
                   responses={status.HTTP_401_UNAUTHORIZED: {'detail': 'string'},
                              status.HTTP_403_FORBIDDEN: {'detail': 'string'},
                              status.HTTP_404_NOT_FOUND: {'detail': 'string'},
                              status.HTTP_429_TOO_MANY_REQUESTS: {'detail': 'string'}})

@router.get('/comments/{task_slug}/',
            summary='Получить все комментарии к задаче')
@inject
async def get_comments(
        task_slug: Annotated[str, Path(
            title='Слаг задачи',
            description='Слаг задачи, по которой получаем комментарии',
        )],
        service: FromDishka[CommentsService]
):
    comments = await service.get_comments(task_slug)
    return comments

@router.post('/comments/',
             status_code=status.HTTP_201_CREATED,
             response_model=dto.ResponseCreateComment,
             summary='Создание комментария')
@inject
async def create_comment(
        comment: Annotated[dto.RequestComment, Body()],
        service: FromDishka[CommentsService],
):
    comment_id = await service.create_comment(comment)
    return comment_id

@router.put('/comments/',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Обновление комментария')
@inject
async def update_comment(
        new_comment: Annotated[dto.UpdateComment, Body()],
        service: FromDishka[CommentsService]
):
    await service.update_comment(new_comment=new_comment)

@router.delete('/comments/{task_slug}/{comment_id}/',
               status_code=status.HTTP_204_NO_CONTENT,
               summary='Удаление комментария')
@inject
async def delete_comment(
        task_slug: Annotated[str, Path(title='Task Slug')],
        comment_id: Annotated[int, Path(title='Comment ID')],
        service: FromDishka[CommentsService]
):
    await service.delete_comment(task_slug=task_slug, comment_id=str(comment_id))
