from langchain.tools import tool
from langchain_core.messages import HumanMessage

from agents.skill_agent import sked_agent
from agents.experience_agent import wexp_agent
from agents.salary_agent import sal_agent


@tool
def call_skill_edu_matcher(resume: str, job_desc: str) -> str:
    """Analyze skill and education fit between resume and job description."""
    response = sked_agent.invoke({
        "messages": [
            HumanMessage(content=f"""
Resume:
{resume}

Job Description:
{job_desc}

Evaluate skill and education fit only.
""")
        ]
    })
    return response["messages"][-1].content


@tool
def call_exp_matcher(resume_exp: str, job_role: str) -> str:
    """Analyze work experience fit for the role."""
    response = wexp_agent.invoke({
        "messages": [
            HumanMessage(content=f"""
Resume Experience:
{resume_exp}

Target Role:
{job_role}

Only analyse Resume experience fit with the job role quickly.
""")
        ]
    })
    return response["messages"][-1].content


@tool
def call_sal_matcher(role: str, location: str, years: float) -> str:
    """Research salary alignment for role, location, and years of experience."""
    response = sal_agent.invoke({
        "messages": [
            HumanMessage(content=f"""
Role: {role}
Location: {location}
Years of Experience: {years}

Estimate market salary alignment.
""")
        ]
    })
    return response["messages"][-1].content
