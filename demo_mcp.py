import asyncio
import logging
from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.server.stdio import stdio_server
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('demo_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

server = Server("demo_mcp")

@server.list_tools()
async def list_tools():
    logger.info("Listing available tools")
    return [
        {
            "name": "greet",
            "description": "Responds with a greeting when receiving 'Hi'",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        }
    ]

@server.call_tool()
async def call_tool(name, arguments):
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    if name == "greet":
        message = arguments.get("message", "").lower()
        if message == "hi":
            logger.info("Received 'Hi', responding with 'Hello'")
            return [{"type": "text", "text": "Hello!"}]
        else:
            logger.info(f"Received message: {message}")
            return [{"type": "text", "text": f"I only respond to 'Hi', but you said: {message}"}]
    
    logger.warning(f"Unknown tool called: {name}")
    return [{"type": "text", "text": "Unknown tool"}]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        start_time = time.time()
        logger.info("Starting demo MCP server")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="demo_mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        end_time = time.time()
        logger.info(f"Time taken to run demo MCP server: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main()) 
