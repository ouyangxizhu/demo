from fastmcp import FastMCP

mcp = FastMCP("weather_server")

@mcp.tool
def get_weather(city: str) -> str:
    return f"{city}天气：晴，阳光明媚"

if __name__ == '__main__':
    mcp.run("streamable-http")

