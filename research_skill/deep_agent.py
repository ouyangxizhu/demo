import os
from pathlib import Path

from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
from deepagents import create_deep_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.chat_models import init_chat_model
from rich import print as rich_print

model = init_chat_model(
    model="gpt-5.5-2026-04-24",                 # model 参数会作为 azure_deployment 使用
    model_provider="azure_openai",
    api_version="2024-03-01-preview",
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    max_tokens=4096,
    max_retries=3,
)
deep_agent = create_deep_agent(
    model=model,
    backend=FilesystemBackend(root_dir= str (Path(__file__).parent)),
    skills=["skills"],
    middleware=[TodoListMiddleware()],
)
result = deep_agent.invoke({
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
#             id='2b5db92c-3a08-42df-b588-a85b7df01fa8'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 123,
#                     'prompt_tokens': 3726,
#                     'total_tokens': 3849,
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
#                 'id': 'chatcmpl-EZSAlyVWNQCbCbpdr4VwZMAVaqufe',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14295-e744-7c61-bc9b-449b075205f4-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 Hello World 
# 技能说明并检查项目文件',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'pending'
#                             },
#                             {
#                                 'content': '查找并运行相关测试',
#                                 'status': 'pending'
#                             },
#                             {
#                                 'content': '汇总修改和测试结果',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_spWqqzNUjj1Jfi8KpU6XwrlT',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 3726,
#                 'output_tokens': 123,
#                 'total_tokens': 3849,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 38}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 Hello World 
# 技能说明并检查项目文件', 'status': 'in_progress'}, {'content': '在 demo.py 
# 中实现 hello_world 函数', 'status': 'pending'}, {'content': 
# '查找并运行相关测试', 'status': 'pending'}, {'content': '汇总修改和测试结果', 
# 'status': 'pending'}]",
#             name='write_todos',
#             id='9c70f800-884f-4727-8103-63b3edb77480',
#             tool_call_id='call_spWqqzNUjj1Jfi8KpU6XwrlT'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 83,
#                     'prompt_tokens': 3899,
#                     'total_tokens': 3982,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 15,
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
#                 'id': 'chatcmpl-EZSAoV6JgdE0BMA06174UWLwVbDXV',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14295-f443-7c70-b032-c9d0de9df0c5-0',
#             tool_calls=[
#                 {
#                     'name': 'read_file',
#                     'args': {
#                         'file_path': '/skills/hello-world-code/SKILL.md',
#                         'limit': 1000
#                     },
#                     'id': 'call_vgocioncuvNmxoB9iAAz9nQa',
#                     'type': 'tool_call'
#                 },
#                 {
#                     'name': 'ls',
#                     'args': {'path': '/'},
#                     'id': 'call_i4G2AkbOTForc7mYeWLISCu0',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 3899,
#                 'output_tokens': 83,
#                 'total_tokens': 3982,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 15}
#             }
#         ),
#         ToolMessage(
#             content='@@ lines 1-12 of 12 @@\n---\nname: 
# hello-world-code\ndescription: Write minimal Hello World code examples. Use when
# the user asks to create, show, or generate Hello World code in a programming 
# language.\n---\n\n# Hello World Code\n\nGenerate the smallest clear runnable 
# Hello World example for the requested programming language.\n\nIf the user does 
# not specify a language, default to Python.\n\nInclude only the code and the 
# minimal run command when useful.',
#             name='read_file',
#             id='c982bd39-9853-4391-a92b-091443147805',
#             tool_call_id='call_vgocioncuvNmxoB9iAAz9nQa'
#         ),
#         ToolMessage(
#             content="['/deep_agent.py', '/skills/']",
#             name='ls',
#             id='b50a79e1-21ff-4942-a412-ebc0497eaf9f',
#             tool_call_id='call_i4G2AkbOTForc7mYeWLISCu0'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 43,
#                     'prompt_tokens': 4092,
#                     'total_tokens': 4135,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 16,
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
#                 'id': 'chatcmpl-EZSArhKooiQsYXZf3ZSdBPZOC8ZBi',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-00ad-7f50-97e8-5cb47200eeba-0',
#             tool_calls=[
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': 'demo.py'},
#                     'id': 'call_fsCLTKfBp9DKqubtHeeLULpX',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4092,
#                 'output_tokens': 43,
#                 'total_tokens': 4135,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 16}
#             }
#         ),
#         ToolMessage(
#             content='No files found',
#             name='glob',
#             id='3ec72c1d-c75d-40cb-bc39-1f2f07857b76',
#             tool_call_id='call_fsCLTKfBp9DKqubtHeeLULpX'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 67,
#                     'prompt_tokens': 4126,
#                     'total_tokens': 4193,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 40,
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
#                 'id': 'chatcmpl-EZSAtOGpEJf5tw6hBdHelAxOsvqSX',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-0875-7df2-8b4c-273896fc9554-0',
#             tool_calls=[
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': '*.py'},
#                     'id': 'call_RGJXH6aIaj8LI8a14ZDdHNAE',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4126,
#                 'output_tokens': 67,
#                 'total_tokens': 4193,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 40}
#             }
#         ),
#         ToolMessage(
#             content="['/deep_agent.py']",
#             name='glob',
#             id='4b13e3e8-714c-4602-8ea5-84d0b5702377',
#             tool_call_id='call_RGJXH6aIaj8LI8a14ZDdHNAE'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 114,
#                     'prompt_tokens': 4163,
#                     'total_tokens': 4277,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 29,
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
#                 'id': 'chatcmpl-EZSAwSciagzgdAKWee8mxMKUtC6qt',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-14d5-7e50-936b-e73c3f6a3773-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 Hello World 
# 技能说明并检查项目文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '查找并运行相关测试',
#                                 'status': 'pending'
#                             },
#                             {
#                                 'content': '汇总修改和测试结果',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_yeZy80gu0MNIWczGbr6aCJ9U',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4163,
#                 'output_tokens': 114,
#                 'total_tokens': 4277,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 29}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 Hello World 
# 技能说明并检查项目文件', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'in_progress'}, {'content': '查找并运行相关测试', 
# 'status': 'pending'}, {'content': '汇总修改和测试结果', 'status': 'pending'}]",
#             name='write_todos',
#             id='009b5829-aa5b-4bfe-8b7f-a00c92fb1526',
#             tool_call_id='call_yeZy80gu0MNIWczGbr6aCJ9U'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 60,
#                     'prompt_tokens': 4336,
#                     'total_tokens': 4396,
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
#                 'id': 'chatcmpl-EZSAzGRkaodG7KZJpJ3AEzT87qkp8',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-1f96-7d23-af75-876ec1cc2af0-0',
#             tool_calls=[
#                 {
#                     'name': 'write_file',
#                     'args': {
#                         'file_path': '/demo.py',
#                         'content': 'def hello_world():\n    return "Hello, 
# World!"\n\n\nif __name__ == "__main__":\n    print(hello_world())\n'
#                     },
#                     'id': 'call_PgE7kwtKlmN5tYgIri2SMkji',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4336,
#                 'output_tokens': 60,
#                 'total_tokens': 4396,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='Updated file /demo.py',
#             name='write_file',
#             id='116e5078-1bbb-424a-91ff-859c7cd4bdeb',
#             tool_call_id='call_PgE7kwtKlmN5tYgIri2SMkji'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 79,
#                     'prompt_tokens': 4412,
#                     'total_tokens': 4491,
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
#                 'id': 'chatcmpl-EZSB1jzj1DeKe4RSI6SFKRuMlPPQj',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-274f-7563-9f7c-8310df85762e-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 Hello World 
# 技能说明并检查项目文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '查找并运行相关测试',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '汇总修改和测试结果',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_F1ArjT2ADDxOhsr9DVXRUpoo',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4412,
#                 'output_tokens': 79,
#                 'total_tokens': 4491,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 Hello World 
# 技能说明并检查项目文件', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'completed'}, {'content': '查找并运行相关测试', 
# 'status': 'in_progress'}, {'content': '汇总修改和测试结果', 'status': 
# 'pending'}]",
#             name='write_todos',
#             id='e34bfab6-aa03-4f61-91e3-7b2c818d9687',
#             tool_call_id='call_F1ArjT2ADDxOhsr9DVXRUpoo'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 95,
#                     'prompt_tokens': 4585,
#                     'total_tokens': 4680,
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
#                 'id': 'chatcmpl-EZSB4p81YB7MOOAkF2J2I9S0mnFhl',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-312a-7730-88f9-e67e5a4d1e65-0',
#             tool_calls=[
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': 'test*.py'},
#                     'id': 'call_5nsZGdv91Ndt48O5bBPiLvFQ',
#                     'type': 'tool_call'
#                 },
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': '*_test.py'},
#                     'id': 'call_tH0ZfGSaj3Mq1AfqdVyWimoU',
#                     'type': 'tool_call'
#                 },
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': '*.toml'},
#                     'id': 'call_XdmX4AioYxMneGxSjOTH0oyx',
#                     'type': 'tool_call'
#                 },
#                 {
#                     'name': 'glob',
#                     'args': {'path': '/', 'pattern': 'requirements*.txt'},
#                     'id': 'call_glRMjenDuFxa0Z8baJOAHEmo',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4585,
#                 'output_tokens': 95,
#                 'total_tokens': 4680,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         ),
#         ToolMessage(
#             content='No files found',
#             name='glob',
#             id='1bdf4649-8a6c-470e-a540-9fdc81faacc6',
#             tool_call_id='call_5nsZGdv91Ndt48O5bBPiLvFQ'
#         ),
#         ToolMessage(
#             content='No files found',
#             name='glob',
#             id='8b1be4bc-6ab1-4a97-8b4b-29e634b49d92',
#             tool_call_id='call_tH0ZfGSaj3Mq1AfqdVyWimoU'
#         ),
#         ToolMessage(
#             content='No files found',
#             name='glob',
#             id='b8a29f6f-b1af-4829-963a-d025ba783836',
#             tool_call_id='call_XdmX4AioYxMneGxSjOTH0oyx'
#         ),
#         ToolMessage(
#             content='No files found',
#             name='glob',
#             id='8156d251-d4c6-44c1-b3a4-f459eaad256b',
#             tool_call_id='call_glRMjenDuFxa0Z8baJOAHEmo'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 348,
#                     'prompt_tokens': 4713,
#                     'total_tokens': 5061,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 318,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 4224,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZSB7IClYakxBKlwmDAV4iuIJPhML',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-3b6f-7602-885a-ecdbe4d210a9-0',
#             tool_calls=[
#                 {
#                     'name': 'read_file',
#                     'args': {'file_path': '/demo.py', 'limit': 100},
#                     'id': 'call_iAg9m29NjQHjvA8IZ3JA8ouM',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4713,
#                 'output_tokens': 348,
#                 'total_tokens': 5061,
#                 'input_token_details': {'audio': 0, 'cache_read': 4224},
#                 'output_token_details': {'audio': 0, 'reasoning': 318}
#             }
#         ),
#         ToolMessage(
#             content='@@ lines 1-6 of 6 @@\ndef hello_world():\n    return 
# "Hello, World!"\n\n\nif __name__ == "__main__":\n    print(hello_world())',
#             name='read_file',
#             id='90ad13b9-5966-437a-88da-619133211d2c',
#             tool_call_id='call_iAg9m29NjQHjvA8IZ3JA8ouM'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 540,
#                     'prompt_tokens': 4785,
#                     'total_tokens': 5325,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 433,
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
#                 'id': 'chatcmpl-EZSBCkFAMlKp3zuaR6OpRIp05jePi',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-51c4-73a3-b3cd-475210b7e499-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 Hello World 
# 技能说明并检查项目文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '查找相关测试文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': 
# '运行测试（当前工具环境缺少命令执行能力，无法完成）',
#                                 'status': 'in_progress'
#                             },
#                             {
#                                 'content': '汇总修改和测试结果',
#                                 'status': 'pending'
#                             }
#                         ]
#                     },
#                     'id': 'call_bqcmuQooGZRctvVAfZ7Ux3Xj',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 4785,
#                 'output_tokens': 540,
#                 'total_tokens': 5325,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 433}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 Hello World 
# 技能说明并检查项目文件', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'completed'}, {'content': '查找相关测试文件', 
# 'status': 'completed'}, {'content': 
# '运行测试（当前工具环境缺少命令执行能力，无法完成）', 'status': 'in_progress'}, 
# {'content': '汇总修改和测试结果', 'status': 'pending'}]",
#             name='write_todos',
#             id='6fbd0d0a-5ef9-4522-be44-2b19c6ac7ff3',
#             tool_call_id='call_bqcmuQooGZRctvVAfZ7Ux3Xj'
#         ),
#         AIMessage(
#             content='',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 227,
#                     'prompt_tokens': 5006,
#                     'total_tokens': 5233,
#                     'completion_tokens_details': {
#                         'accepted_prediction_tokens': None,
#                         'audio_tokens': 0,
#                         'reasoning_tokens': 122,
#                         'rejected_prediction_tokens': None,
#                         'text_tokens': None
#                     },
#                     'prompt_tokens_details': {
#                         'audio_tokens': 0,
#                         'cache_write_tokens': None,
#                         'cached_tokens': 4224,
#                         'image_tokens': None,
#                         'text_tokens': None
#                     }
#                 },
#                 'model_provider': 'openai',
#                 'model_name': 'gpt-5.5-2026-04-24',
#                 'system_fingerprint': None,
#                 'id': 'chatcmpl-EZSBKQ1g5cbCuNiBFEbs9NTmM4KvU',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'tool_calls',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-6da4-7ea3-84bd-a3ba02f52cea-0',
#             tool_calls=[
#                 {
#                     'name': 'write_todos',
#                     'args': {
#                         'todos': [
#                             {
#                                 'content': '读取 Hello World 
# 技能说明并检查项目文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '在 demo.py 中实现 hello_world 函数',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '查找相关测试文件',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': 
# '确认当前工具环境缺少命令执行能力，无法实际运行测试',
#                                 'status': 'completed'
#                             },
#                             {
#                                 'content': '汇总修改和测试结果',
#                                 'status': 'completed'
#                             }
#                         ]
#                     },
#                     'id': 'call_XhvjBqdFXwelnAY2nhIsbvmb',
#                     'type': 'tool_call'
#                 }
#             ],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 5006,
#                 'output_tokens': 227,
#                 'total_tokens': 5233,
#                 'input_token_details': {'audio': 0, 'cache_read': 4224},
#                 'output_token_details': {'audio': 0, 'reasoning': 122}
#             }
#         ),
#         ToolMessage(
#             content="Updated todo list to [{'content': '读取 Hello World 
# 技能说明并检查项目文件', 'status': 'completed'}, {'content': '在 demo.py 中实现 
# hello_world 函数', 'status': 'completed'}, {'content': '查找相关测试文件', 
# 'status': 'completed'}, {'content': 
# '确认当前工具环境缺少命令执行能力，无法实际运行测试', 'status': 'completed'}, 
# {'content': '汇总修改和测试结果', 'status': 'completed'}]",
#             name='write_todos',
#             id='54b7f32c-defe-4b0e-9de7-96f14f5cac87',
#             tool_call_id='call_XhvjBqdFXwelnAY2nhIsbvmb'
#         ),
#         AIMessage(
#             content='已在 `/demo.py` 中创建并实现 `hello_world` 
# 函数：\n\n```python\ndef hello_world():\n    return "Hello, World!"\n\n\nif 
# __name__ == "__main__":\n    
# print(hello_world())\n```\n\n我也查找了测试文件，但当前目录下未发现 `test*.py` 
# 或 `*_test.py` 
# 等测试文件。\n\n另外，当前可用工具环境没有命令执行能力，因此无法实际运行 `python
# demo.py` 或 `pytest`。如果在本地运行，可使用：\n\n```bash\npython 
# /demo.py\n```\n\n预期输出：\n\n```text\nHello, World!\n```',
#             additional_kwargs={'refusal': None},
#             response_metadata={
#                 'token_usage': {
#                     'completion_tokens': 136,
#                     'prompt_tokens': 5223,
#                     'total_tokens': 5359,
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
#                 'id': 'chatcmpl-EZSBNkQ6rbzlLQ96ViL3JELW1aNzs',
#                 'service_tier': 'default',
#                 'prompt_filter_results': None,
#                 'finish_reason': 'stop',
#                 'logprobs': None,
#                 'content_filter_results': {}
#             },
#             id='lc_run--01a14296-7d6e-7510-bd52-66aa44cd7525-0',
#             tool_calls=[],
#             invalid_tool_calls=[],
#             usage_metadata={
#                 'input_tokens': 5223,
#                 'output_tokens': 136,
#                 'total_tokens': 5359,
#                 'input_token_details': {'audio': 0, 'cache_read': 0},
#                 'output_token_details': {'audio': 0, 'reasoning': 0}
#             }
#         )
#     ],
#     'todos': [
#         {
#             'content': '读取 Hello World 技能说明并检查项目文件',
#             'status': 'completed'
#         },
#         {
#             'content': '在 demo.py 中实现 hello_world 函数',
#             'status': 'completed'
#         },
#         {'content': '查找相关测试文件', 'status': 'completed'},
#         {
#             'content': '确认当前工具环境缺少命令执行能力，无法实际运行测试',
#             'status': 'completed'
#         },
#         {'content': '汇总修改和测试结果', 'status': 'completed'}
#     ]
# }
