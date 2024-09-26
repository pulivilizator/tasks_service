import asyncio

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from core.config.config import ConfigModel
from core.enums import Language, HttpRegisterConfirmation
from repository.implementations.bot_repository import BotRepository


@inject
async def handle_register(bot: Bot,
                          hub: FromDishka[TranslatorHub],
                          repository: FromDishka[BotRepository],
                          config: FromDishka[ConfigModel]):
    r = Redis.from_url(config.redis.pubsub_dsn.unicode_string())
    pubsub = r.pubsub()
    await pubsub.subscribe('tg_registration')
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data'].decode()
                user_id, pass_hash = data.split(':', 1)
                lang_r = await repository.get(Language.REDIS_KEY.format(user_id))
                await repository.set_ex(HttpRegisterConfirmation.HASH_KEY.format(user_id), pass_hash, time=10 * 60)
                i18n = hub.get_translator_by_locale(lang_r or 'ru')
                builder = get_kbd(i18n)
                await bot.send_message(chat_id=user_id, text=i18n.setup_password(), reply_markup=builder.as_markup())
    except asyncio.CancelledError:
        await pubsub.unsubscribe('tg_registration')


def get_kbd(i18n):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=i18n.register_yes(),
        callback_data=HttpRegisterConfirmation.YES
    )
    builder.button(
        text=i18n.register_no(),
        callback_data=HttpRegisterConfirmation.NO
    )
    builder.adjust(1)
    return builder