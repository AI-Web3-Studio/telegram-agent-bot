"""
Telegram Bot 客户端入口 / Telegram Bot client entry point
"""
import os
import json
from dotenv import load_dotenv
from fastmcp import Client

# 加载环境变量 / Load environment variables
load_dotenv()

class MCPClient:
    """
    MCP 客户端，基于 fastmcp.Client 封装 / MCP client, wrapper based on fastmcp.Client
    """
    def __init__(self, server_url: str = None, timeout: int = 30):
        # MCP 服务端 URL / MCP server URL
        self.server_url = server_url or os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp-server/mcp/")
        # 超时时间（秒）/ Timeout (seconds)
        self.timeout = timeout

    async def gpt_recommend(self, query: str, limit: int = 1):
        """
        智能商品推荐 / Smart product recommendation
        :param query: 查询内容 / Query string
        :param limit: 返回商品数量 / Number of products to return
        :return: 商品推荐结果 / Product recommendation result
        """
        try:
            async with Client(self.server_url, timeout=self.timeout) as client:
                result = await client.call_tool("gpt_recommend", {"query": query, "limit": limit})
                # 优先返回 data 字段 / Prefer to return the data field first
                if hasattr(result, "data") and result.data is not None:
                    # 尝试解析 JSON / Try to parse JSON
                    try:
                        return json.loads(result.data)
                    except Exception:
                        return result.data
                
                # 兜底返回 result / Fallback to return result
                return result
        except Exception as e:
            # 异常处理 / Exception handling
            return [{"error": f"gpt_recommend error: {e}"}]