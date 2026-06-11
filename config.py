from langchain.chat_models import init_chat_model
from langchain.agents.middleware import ToolRetryMiddleware, ModelRetryMiddleware
from dotenv import load_dotenv

load_dotenv()

# load model
llm = init_chat_model(
    "llama-3.1-8b-instant",
    model_provider="groq",
    temperature=0,
    max_tokens=1000,
)
# model switch for supervisor agent
supervisor_llm = init_chat_model(
    "llama-3.3-70b-versatile",
    model_provider="groq",
    temperature=0,
    max_tokens=1500,
)

# middleware for retries
def default_middleware():
    return [
        ModelRetryMiddleware(max_retries=3),
        ToolRetryMiddleware(
            max_retries=3,
            retry_on=(ConnectionError, TimeoutError),
        ),
    ]
