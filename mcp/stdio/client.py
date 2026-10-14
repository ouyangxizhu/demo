import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich import print as rich_print


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve().with_name("server.py"))],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            rich_print(tools)

            result = await session.call_tool(
                "read_project_config",
                arguments={"name": "mcp"},
            )
            rich_print(result)
                                          
if __name__ == "__main__":
    asyncio.run(main())

# ListToolsResult(
#     meta=None,
#     nextCursor=None,
#     tools=[
#         Tool(
#             name='read_project_config',
#             title=None,
#             description='读取项目配置:param name: 项目名称\n:return: 项目配置',
#             inputSchema={
#                 'additionalProperties': False,
#                 'properties': {'name': {'type': 'string'}},
#                 'required': ['name'],
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
#         TextContent(type='text', text='config for mcp', annotations=None, meta=None)
#     ],
#     structuredContent={'result': 'config for mcp'},
#     isError=False
# )