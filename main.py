import os
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from langchain.agents.middleware import ToolRetryMiddleware, ModelRetryMiddleware
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import create_agent
from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
import tempfile
import streamlit as st


load_dotenv()

llm = init_chat_model(
    "llama-3.1-8b-instant",
    model_provider="groq",
    temperature=0,
    max_tokens=1000
    
)

search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

#skill and education agent
sked_agent = create_agent(
    llm,
    tools=[wikipedia],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(
            max_retries=3,
            retry_on=(ConnectionError,TimeoutError)
        ),
    ],
    system_prompt = '''
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
    '''
)

#work experience agent
wexp_agent = create_agent(
    llm,
    tools=[search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(
            max_retries=3,
            retry_on=(ConnectionError,TimeoutError)
        ),
    ],
    system_prompt = '''
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
    '''
)

#salary agent
sal_agent = create_agent(
    llm,
    tools= [search],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(
            max_retries=3,
            retry_on=(ConnectionError,TimeoutError)
        ),
    ],
    system_prompt = """
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
    )

#skill agent tool
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

#work experience agent tool
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

  Only analyse Resume experience fit with the job role quikly.

  """)
          ]
      })
    return response["messages"][-1].content

#salary agent tool 
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

#supervisor output schema
class ResumeDecision(BaseModel):
    decision: str = Field(description="APPROVE or REJECT")
    score: int = Field(description="Overall score out of 100")
    summary: str = Field(description="Short recruiter-style summary")
    skill_fit: str = Field(description="Skill and education match summary")
    experience_fit: str = Field(description="Experience match summary")
    salary_fit: str = Field(description="Salary alignment summary")

#supervisor agent
sup_agent = create_agent(
    model = llm,
    tools = [call_skill_edu_matcher, call_exp_matcher, call_sal_matcher],
    middleware=[
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(
            max_retries=3,
            retry_on=(ConnectionError,TimeoutError)
        ),
    ],
    system_prompt = '''
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

    Return format:
    DECISION : ACCEPTED OR REJECTED  (RETURN ONLY ONE.)
    SCORE : XXX/100

    Summary : summary of the candidate, Return as bullet points each on a new line using "\n", Do not combine items in one sentence... (maximum words = 50, minimum words = 10)

    Skill fit : RATING:XX/10 (MISSING : in the next line give what is missing from the candidates resume,Return missing items as bullet points,
      one per line.Return each missing skill each on a new line using "\n",Do not combine items in one sentence..) (maximum words = 50, minimum words = 10)

    Experience fit : RATING:XX/10 (NOTES : in the next line give some notes about the candidates experience fit,
    Return as bullet points each on a new line using "\n",Do not combine items in one sentence..) (maximum words = 50, minimum words = 10)

    Salary fit : give the salary range for the experience level of the candidate,Return as bullet points each on a new line using "\n",
    Do not combine items in one sentence.. (maximum words = 50, minimum words = 10)
    '''
)



#document loader
def extract_text_from_uploaded_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    try:
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        text = "\n\n".join(doc.page_content for doc in docs)
        return text
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

#streamlit code
st.title("Resume Analysis Tool")

resume_file = st.file_uploader("Upload Resume PDF", type="pdf")
#jd_file = st.file_uploader("Upload Job Description PDF", type="pdf")
jd_text = st.text_area(
    "Paste Job Description",
    height=500,
    placeholder="Paste the job description here..."
)

if resume_file and jd_text:
    if st.button("Evaluate"):
        resume = extract_text_from_uploaded_pdf(resume_file)
        job_desc = jd_text

        response = sup_agent.invoke({
            "messages": [
                SystemMessage(content='Return the output in that format only, do not add any other outputs like PERCENTAGE HIKE OR CONFIDENCE.' ),
                HumanMessage(
                    content = f'''Screen this resume:\n\n{resume}\n\n Against this job description:\n\n{job_desc}\n\n
                    '''
                
                )
            ]
        })

        st.write("## Resume Screening Result")
        #st.text_area("Model Output", response, height=400)
    
        raw = response["messages"][-1].content

        if raw == None:
            st.error("Could not extract model output")
        else:
            st.markdown(f"```\n{raw}\n```")
