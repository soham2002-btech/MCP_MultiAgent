import asyncio
import os
import logging
from dotenv import load_dotenv
from mcp.server import Server, InitializationOptions, NotificationOptions
import smtplib
import imaplib
import email
from email.message import EmailMessage
from mcp.server.stdio import stdio_server
import time


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('email_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
server = Server("email_mcp")

@server.list_tools()
async def list_tools():
    logger.info("Listing available tools")
    return [
        {
            "name": "send_email",
            "description": "Send an email via SMTP",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["to", "subject", "body"]
            }
        },
        {
            "name": "get_latest_email",
            "description": "Get the latest email from the inbox",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    ]

@server.call_tool()
async def call_tool(name, arguments):
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    if name == "send_email":
        try:
            msg = EmailMessage()
            msg["From"] = os.getenv("EMAIL_USER")
            msg["To"] = arguments["to"]
            msg["Subject"] = arguments["subject"]
            msg.set_content(arguments["body"])
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                smtp.send_message(msg)
            logger.info("Email sent successfully")
            return [{"type": "text", "text": "Email sent successfully!"}]
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
    elif name == "get_latest_email":
        try:
            user = os.getenv("EMAIL_USER")
            password = os.getenv("EMAIL_PASS")
            with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
                mail.login(user, password)
                mail.select("inbox")
                result, data = mail.search(None, "ALL")
                mail_ids = data[0].split()
                if not mail_ids:
                    logger.info("No emails found")
                    return [{"type": "text", "text": "No emails found."}]
                latest_id = mail_ids[-1]
                result, msg_data = mail.fetch(latest_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject = msg["Subject"]
                from_ = msg["From"]
                if msg.is_multipart():
                    body = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                logger.info(f"Retrieved email from: {from_}, subject: {subject}")
                return [{"type": "text", "text": f"From: {from_}\nSubject: {subject}\n\n{body}"}]
        except Exception as e:
            logger.error(f"Failed to get latest email: {e}")
            raise
    logger.warning(f"Unknown tool called: {name}")
    return [{"type": "text", "text": "Unknown tool"}]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        start_time = time.time()
        logger.info("Starting email MCP server")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="email_mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        end_time = time.time()
        logger.info(f"Time taken from start_email_mcp_server: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())
