from pathlib import Path
import subprocess
import os
import sys
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env", override=True)
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from rich import print as rich_print

# @tool
# def read_file(path: str) -> str:
#     """读取 UTF-8 文本文件。"""
#     return Path(path).read_text(encoding="utf-8")

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

# agent = create_agent(
#     model="openai:gpt-5.5",
#     tools=[read_file, write_file, run_tests],
#     middleware=[TodoListMiddleware()],
# )


model = init_chat_model(
    model="gpt-5.5-2026-04-24",                 # model 参数会作为 azure_deployment 使用
    model_provider="azure_openai",
    api_version="2024-03-01-preview",
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    max_tokens=4096,
    max_retries=3,
)
agent = create_agent(
    model=model,
    tools=[write_file, run_tests],
    middleware=[TodoListMiddleware()],
)

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "请先使用 todo list 规划，在 demo.py 中写 hello_world 函数并运行测试",
    }]
})

rich_print("返回结果：",result)
# 返回结果：
# {
#     'messages': [
#         HumanMessage(
#             content='请先使用 todo list 规划，在 demo.py 中写 hello_world
# 函数并运行测试',
#             additional_kwargs={},
#             response_metadata={},
#             id='ed57c23b-4c42-4c97-b4e0-7ce1a082c9d6'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 108,
#                     'prompt_tokens': 1357,
#                     'total_tokens': 1465,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 39,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC22YnQvboKUK9SGQT8TTDnrBYSk',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-2402-7e50-a303-e4330e25d6f9-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '规划并创建 demo.py，定义 hello_world
# 函数',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '运行测试验证 demo.py',
#                                 'status': 'pending'
#                             },
#                             {
#                                 'content': '根据测试结果给出总结',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_bcCqDM6rUzV8ePSRD1M3YChz',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1357,
#                 'output_tokens': 108,
#                 'total_tokens': 1465,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 39}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '规划并创建 demo.py，定义
# hello_world 函数', 'status': 'in_progress'}, {'content': '运行测试验证 demo.py',
# 'status': 'pending'}, {'content': '根据测试结果给出总结', 'status':
# 'pending'}]",
#             name='write_todos',
#             id='8fdfe55c-857f-4b66-90e5-48e289751853',
#             tool_call_id='call_bcCqDM6rUzV8ePSRD1M3YChz'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 36,
#                     'prompt_tokens': 1494,
#                     'total_tokens': 1530,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 0,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 1152,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC247BJKDjElsNgvYbK3h1OuW0DK',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-3392-7dd2-a8f0-39f3e729af1a-0',
#             tool_calls=[
#                 {
#                     'name': 'write_file',
#                     'args': {
#                         'path': 'demo.py',
#                         'content': 'def hello_world():\n    return "Hello,
# World!"\n'
#                     },
#                     'id': 'call_cam4Apmjsj334rszVf26ZWSg',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1494,
#                 'output_tokens': 36,
#                 'total_tokens': 1530,
#                 'input_token_details': {'audio': 0, 'cache_read': 1152},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='wrote demo.py',
#             name='write_file',
#             id='6fde19a2-0baa-4aa2-b561-b086917c003a',
#             tool_call_id='call_cam4Apmjsj334rszVf26ZWSg'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 63,
#                     'prompt_tokens': 1545,
#                     'total_tokens': 1608,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 0,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 1152,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC27yyjVJvDimJ2xBkqh3As764Vj',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-3b5a-7971-b0ae-a173a6962e3f-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '规划并创建 demo.py，定义 hello_world
# 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '运行测试验证 demo.py',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '根据测试结果给出总结',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_JEUziuFe5G4XLb6dU4YIaKk2',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1545,
#                 'output_tokens': 63,
#                 'total_tokens': 1608,
#                 'input_token_details': {'audio': 0, 'cache_read': 1152},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '规划并创建 demo.py，定义
# hello_world 函数', 'status': 'completed'}, {'content': '运行测试验证 demo.py',
# 'status': 'in_progress'}, {'content': '根据测试结果给出总结', 'status':
# 'pending'}]",
#             name='write_todos',
#             id='aae11c08-f5a5-47a6-9c51-d45762029d11',
#             tool_call_id='call_JEUziuFe5G4XLb6dU4YIaKk2'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 18,
#                     'prompt_tokens': 1682,
#                     'total_tokens': 1700,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 0,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 1152,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC29SPkMhJw8TkPUwlpDdr1LIwqm',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-455b-7292-a757-0fda9e9e2860-0',
#             tool_calls=[
#                 {
#                     'name': 'run_tests',
#                     'args': {'path': 'demo.py'},
#                     'id': 'call_i3MA7LgM8mx7qiLNUU4dPMua',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1682,
#                 'output_tokens': 18,
#                 'total_tokens': 1700,
#                 'input_token_details': {'audio': 0, 'cache_read': 1152},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='============================= test session starts
# ==============================\nplatform darwin -- Python 3.13.16, pytest-9.1.1,
# pluggy-1.6.0\nrootdir:
# /Users/bytedance/go/src/code.byted.org/techrooting/demo\nconfigfile:
# pyproject.toml\nplugins: platformdirs-4.13.0, langsmith-0.14.7,
# anyio-4.15.1\ncollected 0 items\n\n============================ no tests ran in
# 0.00s =============================\n',
#             name='run_tests',
#             id='7db35b05-0e0a-4d15-9507-609a9ddd8b3b',
#             tool_call_id='call_i3MA7LgM8mx7qiLNUU4dPMua'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 107,
#                     'prompt_tokens': 1824,
#                     'total_tokens': 1931,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 38,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC2C8lxqTx7cW3MhNxDreVQ4iaae',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-52be-7b60-a1d3-b38fb50b235b-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '规划并创建 demo.py，定义 hello_world
# 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '运行测试验证 demo.py',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '根据测试结果给出总结',
#                                 'status': 'in_progress'
#                             }
#                         ]
#                     },
#                     'id': 'call_raS5fiWBDW8LLdaLPbcSyS7t',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1824,
#                 'output_tokens': 107,
#                 'total_tokens': 1931,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 38}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '规划并创建 demo.py，定义
# hello_world 函数', 'status': 'completed'}, {'content': '运行测试验证 demo.py',
# 'status': 'completed'}, {'content': '根据测试结果给出总结', 'status':
# 'in_progress'}]",
#             name='write_todos',
#             id='2e2941fc-d40e-4132-9a43-1acbc5467075',
#             tool_call_id='call_raS5fiWBDW8LLdaLPbcSyS7t'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 76,
#                     'prompt_tokens': 1961,
#                     'total_tokens': 2037,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 8,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 1152,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC2EizfzTnnrp2diIITH7J1zlK1G',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-5cfa-7172-96d1-e5e43fabab76-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '规划并创建 demo.py，定义 hello_world
# 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '运行测试验证 demo.py',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '根据测试结果给出总结',
#                                 'status': 'completed'
#                             }
#                         ]
#                     },
#                     'id': 'call_zU5yUCYMqMfYKmNOuZvPDjlH',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1961,
#                 'output_tokens': 76,
#                 'total_tokens': 2037,
#                 'input_token_details': {'audio': 0, 'cache_read': 1152},
#                 'output_token_details': {'audio': 0, 'reasoning': 8}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '规划并创建 demo.py，定义
# hello_world 函数', 'status': 'completed'}, {'content': '运行测试验证 demo.py',
# 'status': 'completed'}, {'content': '根据测试结果给出总结', 'status':
# 'completed'}]",
#             name='write_todos',
#             id='4879fa0f-57fa-469e-a96a-8b47167c2f0d',
#             tool_call_id='call_zU5yUCYMqMfYKmNOuZvPDjlH'
#         ),
#         AIMessage(
#             content='已在 `demo.py` 中写入：\n\n```python\ndef hello_world():\n
# return "Hello, World!"\n```\n\n并已运行测试：\n\n```text\ncollected 0 items\nno
# tests ran in
# 0.00s\n```\n\n说明：测试命令执行成功，但当前没有收集到任何测试用例。',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 73,
#                     'prompt_tokens': 2096,
#                     'total_tokens': 2169,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 0,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 1664,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZC2GLOjdJVcG22E5C6GEqoL0GbcT',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'stop',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13ee3-6350-7ca0-a77b-c8ab2925ab59-0',
#             tool_calls=[],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 2096,
#                 'output_tokens': 73,
#                 'total_tokens': 2169,
#                 'input_token_details': {'audio': 0, 'cache_read': 1664},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         )
#     ],
#     'todos': [
#         {
#             'content': '规划并创建 demo.py，定义 hello_world 函数',
#             'status': 'completed'
#         },
#         {'content': '运行测试验证 demo.py', 'status': 'completed'},
#         {'content': '根据测试结果给出总结', 'status': 'completed'}
#     ]
# }
