from fastmcp import FastMCP

mcp = FastMCP("ticket_server")


# Tool：执行操作，客户端通过 call_tool("query_ticket", ...) 调用。
@mcp.tool()
def query_ticket(ticket_id: str) -> str:
    """
    查询票信息:param ticket_id: 票号
    :return: 票信息
    """
    # 模拟查询票信息，真实情况是这里会查询数据库或调用API/RPC接口，这里模拟返回票信息
    return f"ticket {ticket_id}: open"


# Resource：提供可读取的上下文数据，通过 URI 标识；这里的 URI 不是 HTTP 路由。
# 客户端通过 read_resource("ticket://status-guide") 读取。
@mcp.resource("ticket://status-guide")
def ticket_status_guide() -> str:
    """票状态说明，供客户端读取并作为模型的参考资料。"""
    return (
        "票状态说明：\n"
        "- open：待处理。\n"
        "- in_progress：处理中。\n"
        "- closed：已关闭。\n"
        "回复用户时应说明当前状态，不要编造处理进度或完成时间。"
    )


# Prompt：提供可复用的提示词模板，客户端通过 get_prompt(...) 获取。
# 获取模板只会返回消息，不会自动调用工具、读取资源或请求大模型。
@mcp.prompt()
def reply_ticket(ticket_id: str, ticket_info: str, status_guide: str) -> str:
    """根据票号、已查询的票信息和状态说明，生成客服回复提示词。

    Args:
        ticket_id: 票号，例如 123。
        ticket_info: query_ticket 工具返回的票信息。
        status_guide: ticket://status-guide 资源返回的状态说明。
    """
    return (
        "请根据以下资料，用简洁、友好的中文回复查询票状态的用户。\n"
        "仅根据资料说明状态，未知信息请明确告知，不要编造。\n\n"
        f"票号：{ticket_id}\n"
        f"票信息：{ticket_info}\n"
        f"状态说明：\n{status_guide}"
    )


if __name__ == '__main__':
    # 以 streamable-http 传输方式启动 MCP 服务，监听端口 8001
    # MCP 客户端通过 http://localhost:8001/mcp 访问 tools、resources 和 prompts
    mcp.run("streamable-http", host="127.0.0.1", port=8001)
