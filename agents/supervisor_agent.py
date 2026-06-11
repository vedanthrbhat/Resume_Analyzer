from langchain.agents import create_agent
from pydantic import BaseModel, Field

from config import supervisor_llm, default_middleware
from tools.agent_tools import (
    call_skill_edu_matcher,
    call_exp_matcher,
    call_sal_matcher,
)


class ResumeDecision(BaseModel):
    decision: str = Field(description="APPROVE or REJECT")
    score: int = Field(description="Overall score out of 100")
    summary: str = Field(description="Short recruiter-style summary")
    skill_fit: str = Field(description="Skill and education match summary")
    experience_fit: str = Field(description="Experience match summary")
    salary_fit: str = Field(description="Salary alignment summary")


SUPERVISOR_PROMPT = '''
You are a senior recruiting manager screening resumes for shortlisting.

Workflow:
1. Evaluate skill and education fit first.
2. Evaluate experience fit second.
3. Evaluate salary-market alignment third.
4. Make a final decision only after reviewing all three signals.
5. Never call any tool other than the three tools listed above.

Decision rules:
- APPROVE if skills are strong, experience is relevant, and compensation seems aligned.
- REJECT if core requirements are missing or experience is too far from the role.
- Use a score from 0 to 100.
- Be strict, realistic, and concise.

Output a short and structured final decision only.
return the output in the format given below only and do not generate extra format.

IMPORTANT TOOL CALLING RULES:
- You MUST call tools using the structured tool-calling API only.
- NEVER write tool calls as text like <function=name>{...} or ```tool_code```.
- Call each of the three tools exactly once, in order: call_skill_edu_matcher, then call_exp_matcher, then call_sal_matcher.
- After all three tool results are returned, produce the final formatted answer. Do not call any tool again.

Return format:
DECISION : ACCEPTED OR REJECTED  (RETURN ONLY ONE.)
SCORE : XXX/100

Summary : summary of the candidate, Return as bullet points each on a new line using "\n", Do not combine items in one sentence... (maximum words = 50, minimum words = 10)

Skill fit : RATING:XX/10 (MISSING : in the next line give what is missing from the candidates resume,Return missing items as bullet points,
  one per line.Return each missing skill each on a new line using "\n",Do not combine items in one sentence..) (maximum words = 50, minimum words = 10)

Experience fit : RATING:XX/10 (NOTES : in the next line give some notes about the cadidates experience fit,
Return as bullet points each on a new line using "\n",Do not combine items in one sentence..) (maximum words = 50, minimum words = 10)

Salary fit : give the salary range for the experience level of the candidate,Return as bullet points each on a new line using "\n",
Do not combine items in one sentence.. (maximum words = 50, minimum words = 10)
'''

sup_agent = create_agent(
    model=supervisor_llm,
    tools=[call_skill_edu_matcher, call_exp_matcher, call_sal_matcher],
    middleware=default_middleware(),
    system_prompt=SUPERVISOR_PROMPT,
)
