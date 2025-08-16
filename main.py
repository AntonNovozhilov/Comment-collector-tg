import asyncio

from aiogram import Bot, Dispatcher

from commands import command
from config import setting
from handler import handler

bot = Bot(token=setting.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(command)
dp.include_router(handler)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
