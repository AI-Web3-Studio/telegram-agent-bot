"""
日志工具模块 / Logging utilities module
"""
import logging
import sys

def setup_logging():
    """
    配置日志格式和级别，同时写入文件和控制台 / Configure logging format and level, output to file and console
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("chat_logs.txt", encoding="utf-8"),  # 写入文件 / Write to file
            logging.StreamHandler(sys.stdout)  # 控制台输出 / Output to console
        ]
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
