from typing import Annotated

from fastapi import APIRouter, Path, Body, Request
from dishka.integrations.fastapi import FromDishka, inject
from fastapi.params import Depends
from starlette import status

from core import dto
from services.comments_service import CommentsService
from application.dependencies import check_auth

router = APIRouter(tags=['Comment'], dependencies=[Depends(check_auth)])

@router.get('/comments/{task_slug}/')
@inject
async def get_comments(
        task_slug: Annotated[str, Path(
            title='Слаг задачи',
        )],
        service: FromDishka[CommentsService]
):
    comments = await service.get_comments(task_slug)
    return comments

@router.post('/comments/',
             status_code=status.HTTP_201_CREATED,
             response_model=dto.ResponseCreateComment)
@inject
async def create_comment(
        comment: Annotated[dto.RequestComment, Body()],
        service: FromDishka[CommentsService],
):
    comment_id = await service.create_comment(comment)
    return comment_id

@router.put('/comments/',
            status_code=status.HTTP_204_NO_CONTENT)
@inject
async def update_comment(
        new_comment: Annotated[dto.UpdateComment, Body()],
        service: FromDishka[CommentsService]
):
    await service.update_comment(new_comment=new_comment)

@router.delete('/comments/{tusk_slug}/{comment_id}/',
               status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_comment(
        comment_id: Annotated[int, Path(
            title='Идентификатор комментария'
        )],
        tusk_slug: Annotated[str, Path(
            title='Слаг задачи'
        )],
        service: FromDishka[CommentsService]
):
    await service.delete_comment(task_slug=tusk_slug, comment_id=str(comment_id))