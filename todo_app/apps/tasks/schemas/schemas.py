from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

parameters=[
        OpenApiParameter(
            name='Bearer access token',
            location=OpenApiParameter.HEADER,
            type=str,
            description='Токен доступа',
        ),
        OpenApiParameter(
            name='Public key',
            location=OpenApiParameter.HEADER,
            type=bytes,
            description='Публичный ключ',
        ),
        OpenApiParameter(
            name='User tg id',
            location=OpenApiParameter.HEADER,
            type=int,
            description='Телеграм id пользователя',
        ),

    ]

common_task_extend_schema = extend_schema(
    tags=['Task'],
    description='Для авторизации необходим access token либо telegram id + public key\n\n'
                'Если вы авторизовались через swagger, можно ничего не указывать',
    parameters=parameters
)

common_tag_extend_schema = extend_schema(
    tags=['Tag'],
    description='Для авторизации необходим access token либо telegram id + public key\n\n'
                'Если вы авторизовались через swagger, можно ничего не указывать\n\n'
                'Только администраторам доступны методы редактирования, удаления и создания',
    parameters=parameters
)

task_schema = extend_schema_view(
    list = extend_schema(
        summary='Получение задач авторизованного пользователя',
    ),
    create = extend_schema(
        summary='Создать задачу'
    ),
    retrieve = extend_schema(
        summary='Получение конкретной задачи'
    ),
    update = extend_schema(
        summary='Обновление конкретной задачи',
    ),
    destroy = extend_schema(
        summary='Удаление задачи'
    ),
    partial_update=extend_schema(
        summary='Частичное обновление задачи'
    ),
    get_by_tags=extend_schema(
        summary='Получение задач по слагам тэгов',
        parameters=[
            OpenApiParameter(
                name='tag',
                location=OpenApiParameter.QUERY,
                type=str,
                many=True
            )
        ]
    )
)

tag_schema = extend_schema_view(
    list = extend_schema(
        summary='Получение тэгов',
    ),
    create = extend_schema(
        summary='Создать тэг'
    ),
    retrieve = extend_schema(
        summary='Получение конкретного тэга'
    ),
    update = extend_schema(
        summary='Обновление конкретного тэга',
    ),
    destroy = extend_schema(
        summary='Удаление тэга'
    ),
    partial_update=extend_schema(
        summary='Частичное обновление тэга'
    )
)