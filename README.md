# MCP User-Facing Host Chatbot

## Overview
This project implements a user-facing Multi-Component Processor (MCP) host chatbot that routes user commands to various MCP servers based on the request. It leverages the Langchain OpenAI integration and MCP framework to provide a flexible and intelligent command routing system.

The main entry point is `main.py`, which runs an asynchronous chatbot interface. The chatbot listens for user commands, decides which MCP server to route the request to (e.g., GitHub, Email, Demo), and returns the processed results.

## Features
- Routes user commands to different MCP servers (`github_mcp.py`, `email_mcp.py`, `demo_mcp.py`)
- Uses OpenAI GPT-4o-mini model for natural language understanding and routing decisions
- Asynchronous command processing with asyncio
- Logging of user commands, results, and errors to console and `mcp_server.log`
- Environment variable support for OpenAI API key

## Installation

1. Clone the repository or download the source code.

2. Create and activate a Python virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Run the user-facing MCP host chatbot:

```bash
python main.py
```

You will see a prompt to enter commands. Type your command (e.g., "List my GitHub repos") and press Enter. The chatbot will process your request and display the result.

To exit the chatbot, type `exit` or `quit`.

## Logging

Logs are output to the console and saved in `mcp_server.log` in the project directory. Logs include timestamps, log levels, user commands, results, and errors.

## MCP Servers

The user-facing host routes commands to the following MCP servers:

- `github_mcp.py`: Handles GitHub-related commands
- `email_mcp.py`: Handles email-related commands
- `demo_mcp.py`: Demo server for testing and examples

