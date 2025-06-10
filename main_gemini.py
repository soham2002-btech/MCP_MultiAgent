import asyncio
import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPClient, MCPAgent
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mcp_server_gemini.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# --- MCP Host 1: User-Facing MCP Host ---
# This MCP host receives user commands and decides where to route them
USER_HOST_CONFIG = {
    "mcpServers": {
        "githubFacade": {
            "command": "python",
            "args": ["github_mcp.py"]
        },
        "emailFacade": {
            "command": "python",
            "args": ["email_mcp.py"]
        },
        "demoFacade": {
            "command": "python",
            "args": ["demo_mcp.py"]
        }
    }
}

async def user_facing_host():
    logger.info("🚀 Launching User-Facing MCP Host with Gemini...")

    # Client connects to downstream MCPs (e.g., GitHub MCP Facade)
    client = MCPClient.from_dict(USER_HOST_CONFIG)
    prompt = "You are a helpful assistant that can answer questions and help with tasks. based on the user's request, you will decide which MCP to route the request to. you will also decide the best way to route the request to the MCP."
    
    # Initialize Gemini model with correct configuration
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
        convert_system_message_to_human=True
    )
    
    agent = MCPAgent(llm=llm, client=client, max_steps=10, system_prompt=prompt)

    logger.info("🤖 User-Facing MCP Chatbot with Gemini is ready! Type your command (e.g., 'List my GitHub repos'). Type 'exit' to quit.")

    while True:
        user_input = input("\n>> ")
        if user_input.lower() in ["exit", "quit"]:
            logger.info("👋 Exiting. Goodbye!")
            break
        try:
            start_time = time.time()
            logger.info(f"Processing user input: {user_input}")
            result = await agent.run(user_input)
            end_time = time.time()
            logger.info(f"✅ Result:\n{result}")
            logger.info(f"Time taken: {end_time - start_time} seconds")
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(user_facing_host()) 