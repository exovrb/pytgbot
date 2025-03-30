from aiogram import Bot, Dispatcher
import asyncio

from app.handlers import router

async def main():
    bot = Bot(token='7607426185:AAG-9XHukSUjX66JxX3qcVJERuYrgAecs-Y')
    dp = Dispatcher()
    dp.include_router(router) # Включить роутер
    await dp.start_polling(bot) # Внутри диспетчера обращается к серверу тг, а не пришло ли там сообщение

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен') # Убираем ошибку после выключения бота

