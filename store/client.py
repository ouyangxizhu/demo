from pathlib import Path
import subprocess
import os
import sys
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env", override=True)
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langgraph.store.memory import InMemoryStore
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from rich import print as rich_print

@tool
def write_file(path: str, content: str) -> str:
    """写入 UTF-8 文本文件。"""
    Path(path).write_text(content, encoding="utf-8")
    return f"wrote {path}"

@tool
def run_tests(path: str) -> str:
    """运行指定测试文件。"""
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", path],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.stdout + completed.stderr

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[write_file, run_tests],
    middleware=[TodoListMiddleware()],
    store = InMemoryStore(),
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "请先使用 todo list 规划，在 demo.py 中写 hello_world 函数并运行测试",
    }]
})

rich_print("返回结果：",result)