import asyncio
import logging
from idlelib.window import add_windows_to_menu
from pyexpat.errors import messages

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis


logging.basicConfig(level=logging.INFO)

async def handle_register(bot: Bot):
    r = Redis.from_url('redis://localhost:6379/0')
    pubsub = r.pubsub()
    await pubsub.subscribe('tg_registration')
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Да',
        callback_data='1'
    )
    builder.button(
        text="Нет",
        callback_data='0'
    )
    builder.adjust(1)
    try:
        async for message in pubsub.listen():
            print(message)
            if message['type'] == 'message':
                data = message['data'].decode()
                user_id, pass_hash = data.split(':', 1)
                await bot.send_message(chat_id=user_id, text='Хотите установить пароль?', reply_markup=builder.as_markup())
    except asyncio.CancelledError:
        await pubsub.unsubscribe('tg_registration')


async def main():
    bot = Bot(token='6003155169:AAGXnZjCjJjzO9AlzGJUyoxW6P17Y0ufDvY')
    dp = Dispatcher()



    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        asyncio.create_task(handle_register(bot)),
        dp.start_polling(bot),
        return_exceptions=True
    )


if __name__ == '__main__':
    asyncio.run(main())