import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from rich import print as rich_print
from mcp.types import PaginatedRequestParams


async def main() -> None:
    async with streamable_http_client("http://localhost:8001/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            from mcp.types import PaginatedRequestParams

            tools = []
            params = None

            while True:
                page = await session.list_tools(params=params)
                tools.extend(page.tools)

                if page.nextCursor is None:
                    break

                params = PaginatedRequestParams(cursor=page.nextCursor)
                
            rich_print(tools)

            result = await session.call_tool(
                "query_ticket",
                arguments={"ticket_id": "123"},
            )
            rich_print(result)

            # Resource：列出资源，再通过 URI 读取状态说明。
            rich_print(await session.list_resources())
            resource = await session.read_resource("ticket://status-guide")
            rich_print(resource)

            # Prompt：将工具结果和资源内容填入模板，获取可发送给模型的消息。
            rich_print(await session.list_prompts())
            prompt = await session.get_prompt(
                "reply_ticket",
                arguments={
                    "ticket_id": "123",
                    "ticket_info": result.content[0].text,
                    "status_guide": resource.contents[0].text,
                },
            )
            rich_print(prompt)
            # 此处只打印提示词；真正生成客服回复还需要客户端调用大模型。

if __name__ == "__main__":
    asyncio.run(main())

# ListToolsResult(
#     meta=None,
#     nextCursor=None,
#     tools=[
#         Tool(
#             name='query_ticket',
#             title=None,
#             description='查询票信息:param ticket_id: 票号\n:return: 票信息',
#             inputSchema={
#                 'additionalProperties': False,
#                 'properties': {'ticket_id': {'type': 'string'}},
#                 'required': ['ticket_id'],
#                 'type': 'object'
#             },
#             outputSchema={
#                 'properties': {'result': {'type': 'string'}},
#                 'required': ['result'],
#                 'type': 'object',
#                 'x-fastmcp-wrap-result': True
#             },
#             icons=None,
#             annotations=None,
#             meta={'fastmcp': {'tags': []}},
#             execution=None
#         )
#     ]
# )
# CallToolResult(
#     meta={'fastmcp': {'wrap_result': True}},
#     content=[
#         TextContent(type='text', text='ticket 123: open', annotations=None, meta=None)
#     ],
#     structuredContent={'result': 'ticket 123: open'},
#     isError=False
# )
# ListResourcesResult(
#     meta=None,
#     nextCursor=None,
#     resources=[
#         Resource(
#             name='ticket_status_guide',
#             title=None,
#             uri=AnyUrl('ticket://status-guide'),
#             description='票状态说明，供客户端读取并作为模型的参考资料。',
#             mimeType='text/plain',
#             size=None,
#             icons=None,
#             annotations=None,
#             meta={'fastmcp': {'tags': []}}
#         )
#     ]
# )
# ReadResourceResult(
#     meta=None,
#     contents=[
#         TextResourceContents(
#             uri=AnyUrl('ticket://status-guide'),
#             mimeType='text/plain',
#             meta=None,
#             text='票状态说明：\n- open：待处理。\n- in_progress：处理中。\n- 
# closed：已关闭。\n回复用户时应说明当前状态，不要编造处理进度或完成时间。'
#         )
#     ]
# )
# ListPromptsResult(
#     meta=None,
#     nextCursor=None,
#     prompts=[
#         Prompt(
#             name='reply_ticket',
#             title=None,
#             description='根据票号、已查询的票信息和状态说明，生成客服回复提示词。',
#             arguments=[
#                 PromptArgument(
#                     name='ticket_id',
#                     description='票号，例如 123。',
#                     required=True
#                 ),
#                 PromptArgument(
#                     name='ticket_info',
#                     description='query_ticket 工具返回的票信息。',
#                     required=True
#                 ),
#                 PromptArgument(
#                     name='status_guide',
#                     description='ticket://status-guide 资源返回的状态说明。',
#                     required=True
#                 )
#             ],
#             icons=None,
#             meta={'fastmcp': {'tags': []}}
#         )
#     ]
# )
# GetPromptResult(
#     meta=None,
#     description='根据票号、已查询的票信息和状态说明，生成客服回复提示词。',
#     messages=[
#         PromptMessage(
#             role='user',
#             content=TextContent(
#                 type='text',
#                 text='请根据以下资料，用简洁、友好的中文回复查询票状态的用户。\n仅根据资
# 料说明状态，未知信息请明确告知，不要编造。\n\n票号：123\n票信息：ticket 123: 
# open\n状态说明：\n票状态说明：\n- open：待处理。\n- in_progress：处理中。\n- 
# closed：已关闭。\n回复用户时应说明当前状态，不要编造处理进度或完成时间。',
#                 annotations=None,
#                 meta=None
#             )
#         )
#     ]
# )