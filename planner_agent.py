from pydantic import BaseModel, Field
from agents import Agent, WebSearchTool, ModelSettings      # uv add openai-agents
from dotenv import load_dotenv                              # core python lib
import os                                                   # core python lib

load_dotenv(override=True)
MODEL_NAME=os.getenv("DEFAULT_MODEL_NAME")
HOW_MANY_SEARCHES=os.getenv("HOW_MANY_SEARCHES")

INSTRUCTIONS=f"""
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
"""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to this query")
    query: str = Field(description="The search term to use for the web search")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query")

planner_agent = Agent(
    name="Planner Agent",
    instructions=INSTRUCTIONS,
    model=MODEL_NAME,
    output_type=WebSearchPlan
)
