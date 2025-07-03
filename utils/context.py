"""
上下文管理工具 / Context management utilities
"""
from typing import Dict, Any, List

class ContextManager:
    """
    聊天上下文管理器 / Chat context manager
    """
    def __init__(self):
        self._contexts: Dict[int, Dict[str, Any]] = {}
        self._histories: Dict[int, List[dict]] = {}
        self.max_history = 5

    def get(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户上下文 / Get user context
        :param user_id: 用户ID / User ID
        :return: 上下文字典 / Context dict
        """
        return self._contexts.setdefault(user_id, {})

    def set(self, user_id: int, key: str, value: Any):
        """
        设置用户上下文键值 / Set user context key-value
        :param user_id: 用户ID / User ID
        :param key: 键 / Key
        :param value: 值 / Value
        """
        self._contexts.setdefault(user_id, {})[key] = value

    def clear(self, user_id: int):
        """
        清除用户上下文 / Clear user context
        :param user_id: 用户ID / User ID
        """
        if user_id in self._contexts:
            self._contexts[user_id] = {}
        if user_id in self._histories:
            self._histories[user_id] = []

context_manager = ContextManager()


def build_message_context(user_id: int, prompt: str) -> list:
    """
    构建 GPT 聊天上下文，包含 system prompt 和用户历史 / Build GPT chat context with system prompt and user history
    :param user_id: 用户ID / User ID
    :param prompt: 当前用户输入 / Current user input
    :return: 消息上下文列表 / List of message dicts
    """
    # 系统 persona
    system_prompt = {
        "role": "system",
        "content": [{"type": "text", "text": "You are Faye, a friendly and knowledgeable customer support agent dedicated to providing assistance exclusively for the adult products Telegram mini-app and independent store. Support for other scenarios is not available."}]
    }
    # 取历史
    history = context_manager._histories.setdefault(user_id, [])
    history.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    })
    # 只保留最近 max_history 条
    context_manager._histories[user_id] = history[-context_manager.max_history:]
    return [system_prompt] + context_manager._histories[user_id]
