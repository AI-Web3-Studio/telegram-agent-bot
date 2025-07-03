import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from handlers.commands import setup_command_handlers
from handlers.message import setup_message_handler
from utils.logging import setup_logging  # 日志初始化 / Logging setup

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")


async def main():
    setup_logging()  # 初始化日志 / Initialize logging
    # 支持 Windows 下代理
    if PROXY_URL:
        session = AiohttpSession(proxy=PROXY_URL)
        bot = Bot(
            token=TELEGRAM_TOKEN,
            session=session,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
    else:
        bot = Bot(
            token=TELEGRAM_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    dp = Dispatcher()
    setup_command_handlers(dp)
    setup_message_handler(dp)

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
