"""
GPT 服务模块 / GPT Service module
"""
import os
import aiohttp
import asyncio
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# 加载环境变量 / Load environment variables
load_dotenv()

class GPTService:
    """
    只负责与 GPT（OpenAI/Monica）API 的交互。
    """

    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "monica").lower()
        if self.llm_provider == "openai":
            self.api_key: str = os.getenv("OPENAI_API_KEY", "")
            self.api_url: str = "https://api.openai.com/v1/chat/completions"
        else:
            self.api_key: str = os.getenv("MONICA_API_KEY", "")
            self.api_url: str = "https://openapi.monica.im/v1/chat/completions"
        self.proxy_url = os.getenv("PROXY_URL")

    async def ask(self, messages: List[Dict[str, Any]], model: str = "gpt-4o") -> str:
        """
        与 GPT 服务交互，返回回复文本。
        :param messages: 聊天上下文，格式同 OpenAI/Monica API
        :param model: 使用的模型名
        :return: GPT 回复内容
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": model,
            "messages": messages
        }
        timeout = aiohttp.ClientTimeout(total=30)
        proxy = self.proxy_url

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(self.api_url, headers=headers, json=payload, proxy=proxy, ssl=False) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        try:
                            return result["choices"][0]["message"]["content"]
                        except (KeyError, IndexError):
                            return "⚠️ Unexpected response format from LLM API."
                    else:
                        error_text = await resp.text()
                        return f"❌ LLM API request failed: {resp.status}\n{error_text}"
        except asyncio.TimeoutError:
            return "❌ Request to LLM API timed out."
        except Exception as e:
            return f"❌ Error connecting to LLM API: {str(e)}"
