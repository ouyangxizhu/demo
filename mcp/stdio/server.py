from fastmcp import FastMCP

mcp = FastMCP("config_server")

@mcp.tool()
def read_project_config(name: str) -> str:
    """
    读取项目配置:param name: 项目名称
    :return: 项目配置
    """
    return f"config for {name}"

if __name__ == "__main__":
    # Host 启动该进程后，通过 stdin/stdout 与它交换 MCP 消息
    mcp.run(transport="stdio")

