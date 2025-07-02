from setuptools import setup, find_packages

setup(
    name='telegram-agent-bot',
    version='0.1.0',
    description='基于 Telegram 的智能商品推荐机器人，支持 MCP 注册',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot>=13.0',
        'requests>=2.25.0',
        'pytest>=6.0.0',
        'python-dotenv>=0.19.0',
    ],
    python_requires='>=3.7',
)
