from pydantic import BaseModel, Field
from agents import Agent
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL_NAME=os.getenv("DEFAULT_MODEL_NAME")

INSTRUCTIONS="""
You are a senior researcher tasked with writing cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and should be lengthy and detailed.
Aim for 5-10 pages of content, at least 1000 words.
"""
class ReportData(BaseModel):
    short_summary: str = Field()
    markdown_report: str = Field()
    followup_questions: str = Field()

writer_agent = Agent(
    name="Writer Agent", 
    model=MODEL_NAME, 
    instructions=INSTRUCTIONS, 
    output_type=ReportData
)   