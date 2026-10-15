from pathlib import Path
import os
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env", override=True)
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr
from rich import print as rich_print


@tool
def read_file(path: str) -> str:
    """
    读文件
    :param path: 文件路径
    :return: 文件内容
    """
    if not Path(path).exists():
        return f"{path} does not exist"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def write_file(path: str, content: str) -> str:
    """
    写文件
    :param path: 文件路径
    :param content: 文件内容
    :return: 文件最新内容
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content


@tool
def run_tests(path: str) -> str:
    """
    运行测试
    :param path: 文件路径
    :return: 测试结果
    """
    return "success"


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
    tools=[read_file, write_file, run_tests],
    middleware=[TodoListMiddleware()],
)
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "这是一个复杂多步骤任务，请先使用 todo list 规划，再在 demo.py 中写 hello_world 函数并运行测试"}
    ]
})
rich_print("返回结果：",result)
# 返回结果：
# {
#     'messages': [
#         HumanMessage(
#             content='这是一个复杂多步骤任务，请先使用 todo list 规划，再在 
# demo.py 中写 hello_world 函数并运行测试',
#             additional_kwargs={},
#             response_metadata={},
#             id='c14fd7d5-ad73-4094-b7c5-488b86d40a71'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 68,
#                     'prompt_tokens': 1430,
#                     'total_tokens': 1498,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAESDhXjZ6QSNc4thZuVki2QrjA1',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-9e51-7273-8e77-2603243ae30a-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 demo.py 
# 了解现有代码与测试需求',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'pending'
#                             },
#                             {
#                                 'content': '运行测试并根据结果修正',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_zpVh3WKshq10vEClANYQ7lvg',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1430,
#                 'output_tokens': 68,
#                 'total_tokens': 1498,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 demo.py 
# 了解现有代码与测试需求', 'status': 'in_progress'}, {'content': '在 demo.py 
# 中实现 hello_world 函数', 'status': 'pending'}, {'content': 
# '运行测试并根据结果修正', 'status': 'pending'}]",
#             name='write_todos',
#             id='f26e8adf-0830-40d9-bde5-6b753c8c7afb',
#             tool_call_id='call_zpVh3WKshq10vEClANYQ7lvg'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 18,
#                     'prompt_tokens': 1577,
#                     'total_tokens': 1595,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEUUySFJ2ZdlgZjE9G3tUYbZmBy',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-a5b3-7a13-ab67-20344086c010-0',
#             tool_calls=[
#                 {
#                     'name': 'read_file',
#                     'args': {'path': 'demo.py'},
#                     'id': 'call_k63He8LmTGACFxEpfY00xWh9',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1577,
#                 'output_tokens': 18,
#                 'total_tokens': 1595,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='def hell_world():\n    return "hello world"\n',
#             name='read_file',
#             id='2da81e97-6806-4c82-a724-bff35c6598bb',
#             tool_call_id='call_k63He8LmTGACFxEpfY00xWh9'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 68,
#                     'prompt_tokens': 1616,
#                     'total_tokens': 1684,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEWT5AdBCzL9no3kif02oxQx2ma',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-aba6-75e3-a4d6-cb4da42f42c0-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 demo.py 
# 了解现有代码与测试需求',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '运行测试并根据结果修正',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_MJ6KdeMmxVOUx9DAXGUdi9ER',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1616,
#                 'output_tokens': 68,
#                 'total_tokens': 1684,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 demo.py 
# 了解现有代码与测试需求', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'in_progress'}, {'content': 
# '运行测试并根据结果修正', 'status': 'pending'}]",
#             name='write_todos',
#             id='9ba93359-4fdb-4a3f-8b98-166f65de8506',
#             tool_call_id='call_MJ6KdeMmxVOUx9DAXGUdi9ER'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 34,
#                     'prompt_tokens': 1763,
#                     'total_tokens': 1797,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEXfWw1mYawLRwiXz9TlGbdMxt6',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-b24e-7862-9c4d-ecca5338d8d7-0',
#             tool_calls=[
#                 {
#                     'name': 'write_file',
#                     'args': {
#                         'path': 'demo.py',
#                         'content': 'def hello_world():\n    return "hello 
# world"\n'
#                     },
#                     'id': 'call_XDBCaI8L5gEhKE9iQxC6ccu8',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1763,
#                 'output_tokens': 34,
#                 'total_tokens': 1797,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='def hello_world():\n    return "hello world"\n',
#             name='write_file',
#             id='6604692f-4f05-4590-b1b4-df37f27988bd',
#             tool_call_id='call_XDBCaI8L5gEhKE9iQxC6ccu8'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 68,
#                     'prompt_tokens': 1818,
#                     'total_tokens': 1886,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEa8yspPHHiOGybHFkRLBwSbw1V',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-bb2e-7581-bc5c-e1aaa2ec5477-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 demo.py 
# 了解现有代码与测试需求',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '运行测试并根据结果修正',
#                                 'status': 'in_progress'
#                             }
#                         ]
#                     },
#                     'id': 'call_AbcvzRFtjCKaslnCsCRCZtmH',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1818,
#                 'output_tokens': 68,
#                 'total_tokens': 1886,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 demo.py 
# 了解现有代码与测试需求', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'completed'}, {'content': '运行测试并根据结果修正',
# 'status': 'in_progress'}]",
#             name='write_todos',
#             id='f673fa37-d34e-403c-9d58-bed9e81b0836',
#             tool_call_id='call_AbcvzRFtjCKaslnCsCRCZtmH'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 18,
#                     'prompt_tokens': 1965,
#                     'total_tokens': 1983,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEbPE2RrYHxy7q3XMvyjOYtKqfQ',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-c2a2-73a1-8a7d-4094db529b11-0',
#             tool_calls=[
#                 {
#                     'name': 'run_tests',
#                     'args': {'path': 'demo.py'},
#                     'id': 'call_ew1hQf3AeTzyoqtbjm8FkJwo',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1965,
#                 'output_tokens': 18,
#                 'total_tokens': 1983,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='success',
#             name='run_tests',
#             id='87768d98-1116-4de5-9057-320837495160',
#             tool_call_id='call_ew1hQf3AeTzyoqtbjm8FkJwo'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 67,
#                     'prompt_tokens': 1995,
#                     'total_tokens': 2062,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEeQo0xk5dbPqFcvmeJ6IjsXikQ',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-cbb2-7282-861a-3500f8d44a12-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 demo.py 
# 了解现有代码与测试需求',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '运行测试并根据结果修正',
#                                 'status': 'completed'
#                             }
#                         ]
#                     },
#                     'id': 'call_9IiRi5jxdjyH8rzYh3OUFZFO',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 1995,
#                 'output_tokens': 67,
#                 'total_tokens': 2062,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 demo.py 
# 了解现有代码与测试需求', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'completed'}, {'content': '运行测试并根据结果修正',
# 'status': 'completed'}]",
#             name='write_todos',
#             id='ee1f14cf-312a-4b65-b08c-ac03cde7957c',
#             tool_call_id='call_9IiRi5jxdjyH8rzYh3OUFZFO'
#         ),
#         AIMessage(
#             content='已完成：\n\n- 已使用 todo list 规划任务\n- 已在 `demo.py` 
# 中实现 `hello_world` 函数：\n\n```python\ndef hello_world():\n    return "hello 
# world"\n```\n\n- 已运行测试，结果：`success`',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 57,
#                     'prompt_tokens': 2140,
#                     'total_tokens': 2197,
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
#                         'cached_tokens': 0,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZAEhyX8ABm6D9dVYAX5NcSrpqyaq',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'stop',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a13e79-d636-7d93-a6ef-c32bdca5d4d1-0',
#             tool_calls=[],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 2140,
#                 'output_tokens': 57,
#                 'total_tokens': 2197,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         )
#     ],
#     'todos': [
#         {
#             'content': '读取 demo.py 了解现有代码与测试需求',
#             'status': 'completed'
#         },
#         {
#             'content': '在 demo.py 中实现 hello_world 函数',
#             'status': 'completed'
#         },
#         {'content': '运行测试并根据结果修正', 'status': 'completed'}
#     ]
# }
# todo list:
# [
#     {'content': '读取 demo.py 了解现有代码与测试需求', 'status': 'completed'},
#     {'content': '在 demo.py 中实现 hello_world 函数', 'status': 'completed'},
#     {'content': '运行测试并根据结果修正', 'status': 'completed'}
# ]
