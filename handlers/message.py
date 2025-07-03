import logging
import os
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from utils.context import build_message_context
from utils.logging import log_chat
from gpt_service import GPTService
from client import MCPClient

ASSETS_URL_PREFIX = os.getenv("ASSETS_URL_PREFIX", "")  # 资源前缀 / Asset URL prefix
SHOP_URL = os.getenv("SHOP_URL", "")  # Miniapp商品详情前缀 / Miniapp product detail URL prefix

def setup_message_handler(dp):
    """
    注册消息处理器 / Register message handler
    """
    @dp.message()
    async def handle_message(message: Message):
        """
        处理所有用户消息 / Handle all user messages
        """
        user_id = message.from_user.id  # 用户ID / User ID
        user_text = message.text.strip()  # 用户输入文本 / User input text
        # 用 GPT 判断是否在找商品（不带历史，仅当前消息）/ Use GPT to determine if user is searching for a product (no history, only current message)
        judge_prompt = f"Is the user trying to find or buy a product with this message? Only answer 'yes' or 'no': {user_text}"
        judge_messages = [{
            "role": "user",
            "content": [{"type": "text", "text": judge_prompt}]
        }]
        gpt = GPTService()
        judge_result = await gpt.ask(judge_messages)
        if "yes" in judge_result.strip().lower():
            # 是找商品，调用 MCP 推荐 / If searching for product, call MCP recommendation
            mcp = MCPClient()
            products = await mcp.gpt_recommend(user_text, limit=1)
            reply = ""
            if isinstance(products, list) and products:
                prod = products[0]
                title = prod.get("title", "")
                price = prod.get("price", "")
                compare_at_price = prod.get("compare_at_price", "")
                desc = prod.get("description", "")
                cover = prod.get("cover", "")
                product_id = prod.get("id", "")
                # 拼接资源前缀 / Add asset prefix if needed
                if cover and not (cover.startswith("http://") or cover.startswith("https://")):
                    cover = ASSETS_URL_PREFIX.rstrip("/") + "/" + cover.lstrip("/")
                # 第一行：标题 价格 划线原价（美元）/ First line: title, price, compare price (USD)
                first_line = f"<b>{title}</b>  <b>${price}</b>"
                if compare_at_price:
                    first_line += f" <s>${compare_at_price}</s>"
                caption = f"{first_line}\n{desc}"
                # 构建"View Details"按钮 / Build "View Details" button
                detail_url = f"{SHOP_URL}?startapp=product_{product_id}" if product_id else SHOP_URL
                keyboard = None
                if detail_url:
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [InlineKeyboardButton(text="View Details", url=detail_url)]
                        ]
                    )
                if cover:
                    await message.answer_photo(photo=cover, caption=caption, parse_mode="HTML", reply_markup=keyboard)
                    reply = f"[Image Recommendation] {caption}"
                else:
                    await message.answer(caption, parse_mode="HTML")
                    reply = caption
            else:
                await message.answer(str(products), parse_mode="HTML")
                reply = str(products)
        else:
            # 不是找商品，正常 GPT 聊天 / Not searching for product, normal GPT chat
            messages = build_message_context(user_id, user_text)
            reply = await gpt.ask(messages)
            await message.answer(reply)
        log_chat(user_id, user_text, reply)  # 记录对话 / Log the conversation
