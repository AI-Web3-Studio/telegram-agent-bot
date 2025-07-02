import os
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from utils.logging import log_chat

SHOP_URL = os.getenv("SHOP_URL")  # 商品页URL / Shop page URL
SERVICE_URL = os.getenv("SERVICE_URL")  # 客服URL / Customer service URL
SERVICE_USERNAME = os.getenv("SERVICE_USERNAME")  # 客服用户名 / Customer service username
POLICY_URL = os.getenv("POLICY_URL")  # 隐私政策URL / Policy URL

# --- 命令处理器 ---


def setup_command_handlers(dp):
    """
    注册所有命令处理器 / Register all command handlers
    """
    @dp.message(CommandStart())
    async def start_handler(message: Message):
        """/start 命令处理 / Handle /start command"""
        keyboard = [[InlineKeyboardButton(text="🛍️ Shop Now", url=SHOP_URL)]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("🔞Ready to unlock some fun? 💋Welcome to your pleasure corner.", reply_markup=reply_markup)
        log_chat(message.from_user.id, "/start", "Welcome message sent.")

    @dp.message(Command("trackorder"))
    async def trackorder_handler(message: Message):
        """/trackorder 命令处理 / Handle /trackorder command"""
        await message.answer("📦 Please enter your order number to check the tracking information.")
        log_chat(message.from_user.id, "/trackorder", "Asked for order number.")

    @dp.message(Command("help"))
    async def help_handler(message: Message):
        """/help 命令处理 / Handle /help command"""
        help_text = (
            "🤖 <b>Bot Commands</b>\n"
            "/start - Start interacting with the bot\n"
            "/shop - Browse Products\n"
            "/trackorder - Check order tracking information\n"
            "/help - Get help or view FAQs\n"
            "/contact - Contact customer service\n"
            "/language - Switch language\n"
            "/policy - View privacy policy and user agreement\n"
            "/feedback - Submit feedback or reviews\n"
        )
        await message.answer(help_text, parse_mode="HTML")
        log_chat(message.from_user.id, "/help", "Help message sent.")

    @dp.message(Command("contact"))
    async def contact_handler(message: Message):
        """/contact 命令处理 / Handle /contact command"""
        await message.answer(
            f"☎️ Customer Service: <a href=\"{SERVICE_URL}\">@{SERVICE_USERNAME}</a>\nYou can also leave a message here and we will get back to you as soon as possible.",
            parse_mode="HTML"
        )
        log_chat(message.from_user.id, "/contact", f"Contact info sent: @{SERVICE_USERNAME}")

    @dp.message(Command("language"))
    async def language_handler(message: Message):
        """/language 命令处理 / Handle /language command"""
        keyboard = [[
            InlineKeyboardButton(text="English", callback_data="lang_en"),
            InlineKeyboardButton(text="Русский", callback_data="lang_ru")
        ]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("🌐 Please select your language:", reply_markup=reply_markup)
        log_chat(message.from_user.id, "/language", "Language selection shown.")

    @dp.message(Command("policy"))
    async def policy_handler(message: Message):
        """/policy 命令处理 / Handle /policy command"""
        await message.answer(f"🔒 <b>Privacy Policy & User Agreement</b>\n{POLICY_URL}", parse_mode="HTML")
        log_chat(message.from_user.id, "/policy", "Policy info sent.")

    @dp.message(Command("feedback"))
    async def feedback_handler(message: Message):
        """/feedback 命令处理 / Handle /feedback command"""
        await message.answer("📝 Please type your feedback or review and send it. We value your input!")
        log_chat(message.from_user.id, "/feedback", "Feedback prompt sent.")

    @dp.message(Command("shop"))
    async def shop_handler(message: Message):
        """/shop 命令处理 / Handle /shop command"""
        keyboard = [[InlineKeyboardButton(text="🛍️ Shop Now", url=SHOP_URL)]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        await message.answer("🛍️ Click the button below to browse products:", reply_markup=reply_markup)
        log_chat(message.from_user.id, "/shop", "Shop link sent.")
