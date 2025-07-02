"""
日志工具模块 / Logging utilities module
"""
import logging
import sys

def setup_logging():
    """
    配置日志格式和级别 / Configure logging format and level
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        stream=sys.stdout
    )

def log_chat(user_id, action, detail=None):
    """
    记录用户操作日志 / Log user action
    :param user_id: 用户ID / User ID
    :param action: 操作 / Action
    :param detail: 详情 / Detail
    """
    msg = f"[User:{user_id}] {action}"
    if detail:
        msg += f" | {detail}"
    logging.info(msg)
