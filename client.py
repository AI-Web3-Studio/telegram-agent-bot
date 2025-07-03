"""
Telegram Bot 客户端入口 / Telegram Bot client entry point
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from handlers import commands, message
from utils.logging import setup_logging

# 加载环境变量 / Load environment variables
load_dotenv()

# 设置日志 / Set up logging
setup_logging()

# 读取 Telegram Token / Read Telegram Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 初始化 Bot 和 Dispatcher / Initialize Bot and Dispatcher
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# 注册命令处理器 / Register command handlers
commands.setup_command_handlers(dp)
# 注册消息处理器 / Register message handlers
message.setup_message_handlers(dp)

async def set_bot_commands():
    """
    设置 Bot 命令菜单 / Set Bot command menu
    """
    commands_list = [
        BotCommand(command="start", description="Start the bot / 启动机器人"),
        BotCommand(command="shop", description="Browse products / 浏览商品"),
        BotCommand(command="trackorder", description="Track your order / 查询订单"),
        BotCommand(command="help", description="Help / 帮助"),
        BotCommand(command="contact", description="Contact service / 联系客服"),
        BotCommand(command="language", description="Switch language / 切换语言"),
        BotCommand(command="policy", description="Privacy policy / 隐私政策"),
        BotCommand(command="feedback", description="Feedback / 反馈")
    ]
    await bot.set_my_commands(commands_list)

async def main():
    """
    启动 Telegram Bot / Start Telegram Bot
    """
    await set_bot_commands()
    logging.info("Bot started. Listening for messages... / 机器人已启动，等待消息...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 