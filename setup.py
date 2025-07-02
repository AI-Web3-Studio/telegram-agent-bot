from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="telegram-agent-bot",
    version="0.1.0",
    description="Open-source, extensible Telegram bot for product recommendation and AI-powered chat (MCP, LLM, plugin, async)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI-Web3-Studio",
    url="https://github.com/AI-Web3-Studio/telegram-agent-bot.git",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "aiogram>=3.0.0",
        "aiohttp_socks>=0.7.1",
        "python-dotenv>=0.19.0",
        "pytest>=6.0.0",
        "fastmcp>=0.2.0",
        "openai>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "telegram-agent-bot=client:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP"
    ],
    keywords="telegram bot, ai, product recommendation, mcp, llm, plugin, async, openai, monica, chatbot, e-commerce, agent",
)
