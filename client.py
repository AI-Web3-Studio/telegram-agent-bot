"""
Telegram Bot 客户端入口 / Telegram Bot client entry point
"""
import os
import json
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.utilities.types import MCPContent

# 加载环境变量 / Load environment variables
load_dotenv()

class MCPClient:
    """
    MCP 客户端，基于 fastmcp.Client 封装
    """
    def __init__(self, server_url: str = None, timeout: int = 30):
        self.server_url = server_url or os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp-server/mcp/")
        self.timeout = timeout

    async def gpt_recommend(self, query: str, limit: int = 1):
        try:
            async with Client(self.server_url, timeout=self.timeout) as client:
                result = await client.call_tool("gpt_recommend", {"query": query, "limit": limit})
                if isinstance(result, list) and all(isinstance(item, MCPContent) for item in result):
                    products = []
                    for item in result:
                        try:
                            products.extend(json.loads(item.text))
                        except Exception as e:
                            products.append({"error": f"parse json error: {e}", "raw": item.text})
                    return products
                return result
        except Exception as e:
            return [{"error": f"gpt_recommend error: {e}"}]