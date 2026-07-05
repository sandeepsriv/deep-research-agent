from agents import Agent, WebSearchTool, ModelSettings      # uv add openai-agents
from dotenv import load_dotenv                              # core python lib
import os                                                   # core python lib

load_dotenv(override=True)
MODEL_NAME=os.getenv("DEFAULT_MODEL_NAME")

INSTRUCTIONS="""
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 words.
Capture the main points and be succint. Reply only with the summary. 
"""

settings=ModelSettings(tool_choice="required")
tools=[WebSearchTool()]         # List of tools

search_agent = Agent(
    name="Search Agent", 
    instructions=INSTRUCTIONS, 
    model=MODEL_NAME, 
    tools=tools, 
    model_settings=settings 
)
