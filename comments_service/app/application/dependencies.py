from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import Header, Depends, Security
from fastapi.security import APIKeyHeader
from starlette.requests import Request

from services.comments_service import CommentsService


@inject
async def check_auth(service: FromDishka[CommentsService],
                     request: Request,
                     bearer_token: Annotated[str, Security(APIKeyHeader(name='Authorization', auto_error=False))] = None,
                     public_key: Annotated[str, Header(alias='x-public-key',
                                                       title='Публичный ключ',
                                                       description='public key для авторизации в сервисе')] = None,
                     tg_id: Annotated[str, Header(alias='x-tg-id',
                                                  description='tg id пользователя для которого делается запрос')] = None):
    headers = dict(request.headers)
    cookies = request.cookies
    task_slug = request.path_params.get('task_slug')
    if not task_slug:
        body = await request.json()
        task_slug = body.get('task_slug')
    await service.check_task_auth(headers=headers, cookies=cookies, task_slug=task_slug)
