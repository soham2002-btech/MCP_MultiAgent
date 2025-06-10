import subprocess
import os
import logging
from dotenv import load_dotenv
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('github_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

def start_github_mcp_server():
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN not set in .env file")
        raise ValueError("GITHUB_TOKEN not set in .env file")

    logger.info("🔁 Launching GitHub MCP Host via npx...")
    
    start_time = time.time()
    try:
        subprocess.run([
            "npx",
            "-y",
            "@modelcontextprotocol/server-github",
            "--token",
            github_token
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start GitHub MCP server: {e}")
        raise
    end_time = time.time()
    logger.info(f"Time taken from start_github_mcp_server: {end_time - start_time} seconds")

if __name__ == "__main__":
    start_github_mcp_server()
