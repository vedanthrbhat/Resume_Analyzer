from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun

from config import llm, default_middleware

search = DuckDuckGoSearchRun()

EXPERIENCE_PROMPT = """
You are a resume evaluation assistant focused on work experience matching.

Use web search only for public market or role-context references when needed.
Do not invent experience. Only infer from the resume and job description.

Task:
- Compare years of experience, role alignment, seniority, and domain fit.
- Highlight relevant companies, titles, and scope.
- Return a concise experience fit summary.

Return format:
FIT: XX%
COMPANIES: [list]
ROLES: [list]
RATING: X/10
NOTES: short explanation
"""

wexp_agent = create_agent(
    llm,
    tools=[search],
    middleware=default_middleware(),
    system_prompt=EXPERIENCE_PROMPT,
)
