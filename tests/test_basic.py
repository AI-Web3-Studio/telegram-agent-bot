"""
基础功能测试 / Basic functionality tests
"""
import pytest
from utils.context import context_manager, build_message_context
from utils.logging import setup_logging, log_chat
from gpt_service import GPTService


def test_context_manager():
    """
    测试上下文管理器 / Test context manager
    """
    user_id = 123
    context_manager.set(user_id, "foo", "bar")
    assert context_manager.get(user_id)["foo"] == "bar"
    context_manager.clear(user_id)
    assert context_manager.get(user_id) == {}


def test_logging(caplog):
    """
    测试日志记录 / Test logging
    """
    setup_logging()
    with caplog.at_level("INFO"):
        log_chat(1, "test_action", "test_detail")
    assert any("test_action" in m for m in caplog.messages)


def test_build_message_context():
    user_id = 123
    prompt = "Hello, I want to buy something."
    context = build_message_context(user_id, prompt)
    assert isinstance(context, list)
    assert context[0]["role"] == "system"
    assert context[-1]["role"] == "user"
    assert context[-1]["content"][0]["text"] == prompt


def test_log_chat(caplog):
    setup_logging()
    with caplog.at_level("INFO"):
        log_chat(123, "hi", "hello")
    assert "[User:123] hi | hello" in caplog.text


def test_gpt_service_init():
    gpt = GPTService()
    assert hasattr(gpt, "ask")
    assert gpt.api_url
