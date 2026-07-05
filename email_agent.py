from pydantic import BaseModel, Field
from agents import Agent, function_tool, ModelSettings
from dotenv import load_dotenv
import os
from messenger import send_email, push

load_dotenv(override=True)
MODEL_NAME=os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini")
settings = ModelSettings(tool_choice="required")

USE_EMAIL = False

@function_tool
def send_email_tool(subject:str, text_body:str, html_body: str):
    """
    Send out an email with the given subject and body
    
    Args:
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email
    
    """

    if USE_EMAIL:
        print(subject, text_body, html_body)
    else:
        print(f"Subject: {subject}\n\n{text_body}")
    return "Email sent successfully"

INSTRUCTIONS = """
You are provided with a detailed report. Use your tool to send an email, converting the report into
a clean, well presented HTML email with an appropriate subject line.
"""

email_agent = Agent(
    name="Email Agent",
    model=MODEL_NAME,
    instructions=INSTRUCTIONS,
    tools=[send_email_tool],
    model_settings=settings
)

