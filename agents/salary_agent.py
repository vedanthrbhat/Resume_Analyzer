from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

from config import llm, default_middleware

search = DuckDuckGoSearchRun()

SALARY_PROMPT = """
You are a compensation research assistant.

Use web search only for public salary-market context.
Do not guess salary. If exact salary data is unavailable, provide an estimated range and clearly label it as an estimate.

Task:
- Estimate market-aligned salary range for the role, location, and years of experience.
- Mention confidence level and whether the profile seems above, below, or aligned with the market.

Return format:
RANGE: X - Y LPA
PERCENTAGE HIKE: XX%
CONFIDENCE: LOW/MEDIUM/HIGH
NOTES: short explanation
"""

sal_agent = create_agent(
    llm,
    tools=[search],
    middleware=default_middleware(),
    system_prompt=SALARY_PROMPT,
)
