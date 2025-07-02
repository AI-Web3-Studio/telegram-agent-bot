"""
上下文管理工具 / Context management utilities
"""
from typing import Dict, Any

class ContextManager:
    """
    聊天上下文管理器 / Chat context manager
    """
    def __init__(self):
        self._contexts: Dict[int, Dict[str, Any]] = {}

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

context_manager = ContextManager()
