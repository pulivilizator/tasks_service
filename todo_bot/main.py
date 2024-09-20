import asyncio

from aiogram import Bot, Dispatcher
from redis.asyncio import Redis


async def handle_register(bot: Bot):
    r = Redis.from_url('redis://localhost:6379/3')
    pubsub = r.pubsub()
    pubsub.subscribe('tg_registration')

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode()
            user_id, pass_hash = data.split(':', 1)
            await bot.send_message(user_id, 'Хотите установить пароль?')

async def main():
    bot = Bot(token='6003155169:AAGXnZjCjJjzO9AlzGJUyoxW6P17Y0ufDvY')
    dp = Dispatcher()

    await asyncio.create_task(handle_register(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())