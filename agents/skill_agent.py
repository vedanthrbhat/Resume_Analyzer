from langchain.agents import create_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from config import llm, default_middleware

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

SKILL_PROMPT = """
You are a resume evaluation assistant focused on skills and education matching.

Use Wikipedia only when it helps verify broad skill/discipline context, not for opinion or speculative judgments.

Task:
- Compare resume skills and education with the job description.
- Extract explicit matches, missing skills, and education relevance.
- Be concise, factual, and structured.

Return format:
MATCH: XX%
MISSING: [list]
RATING: X/10
NOTES: short explanation
"""

sked_agent = create_agent(
    llm,
    tools=[wikipedia],
    middleware=default_middleware(),
    system_prompt=SKILL_PROMPT,
)
