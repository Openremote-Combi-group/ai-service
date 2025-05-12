# server.py
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="OpenRemote")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"calculated result: {(a + b) * 10}")
    return (a + b) * 10

# Add an addition tool
@mcp.tool()
def write_file(file_name: str, content: str):
    """Create a file, and write some content into it"""
    open(file_name, "w").write(content)


# Add a dynamic greeting resource
@mcp.resource("system://info")
def system_info() -> str:
    """Get system info"""
    return f"CPU: Ryzen 5000 Series!"


if __name__ == "__main__":
    mcp.run()