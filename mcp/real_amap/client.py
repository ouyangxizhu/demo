import asyncio
import os
from urllib.parse import urlencode

from dotenv import load_dotenv, find_dotenv
from pydantic import SecretStr

load_dotenv(find_dotenv(), override=True)
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

from rich import print as rich_print

# 高德地图的api_key https://console.amap.com/dev/key/app
# MCP接入说明 https://lbs.amap.com/api/mcp-server/gettingstarted
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
# https://platform.deepseek.com/获取
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "DeepSeek-V4.1-Flash")


def build_amap_mcp_url() -> str:
    """
    根据高德官方格式构造 Streamable HTTP MCP 地址。

    使用 urlencode，而不是直接进行字符串拼接。
    注意：不要打印该 URL，否则可能泄露高德 Key。
    """
    query_string = urlencode({"key": AMAP_API_KEY})
    return f"https://mcp.amap.com/mcp?{query_string}"


async def main() -> None:
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("请先在 .env 中配置 DEEPSEEK_API_KEY")

    model = init_chat_model(
        model=DEEPSEEK_MODEL,
        model_provider="deepseek",
        api_key=SecretStr(DEEPSEEK_API_KEY),
    )
    mcp_config = {
        # 这里可以配置多个 MCP 服务，每个服务可以提供多个工具。
        "amap": {
            "url": build_amap_mcp_url(),
            "transport": "http",
        },
    }

    # 客户端自动管理会话，并为工具名添加服务名前缀，避免同名冲突。
    client = MultiServerMCPClient(mcp_config, tool_name_prefix=True)
    tools = await client.get_tools()
    rich_print("已加载高德 MCP 工具列表：", tools)

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
你是一个使用高德地图 MCP 工具的出行规划助手。

请遵循以下规则：
1. 涉及地址、地点、坐标、距离、天气或路线时，优先调用高德 MCP 工具。
2. 不要凭记忆猜测坐标、距离、行驶时间或路线。
3. 地点存在歧义时，先使用地点搜索工具确认；仍无法确认时再询问用户。
4. 规划路线时，应先确认起点和终点，再选择对应的驾车、步行、骑行或公交工具。
5. 最终回答应简洁说明距离、预计时间、推荐方案和必要注意事项。
6. 路线和时间可能受实时交通影响，应提醒用户以实际导航为准。
7. 不得输出、复述或泄露任何 API Key、MCP 连接地址或认证信息。
""",
    )

    question = "帮我规划从北京南站到故宫博物院的驾车路线，并说明距离和预计时间。"

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )


    rich_print("agent全部返回：", result)
    final_message = result["messages"][-1]
    rich_print("最终回答：", final_message.content)


if __name__ == "__main__":
    asyncio.run(main())
