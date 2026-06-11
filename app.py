import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from groq import BadRequestError
from styles import inject_css
from pdf_utils import extract_text_from_uploaded_pdf
from parser import parse_agent_output
from agents import sup_agent


# ---------- Page config (must be first Streamlit call) ----------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### ⚙️ About")
    st.markdown(
        "This **AI Resume Analyzer** uses a multi-agent system to evaluate candidates against a job description."
    )
    st.markdown("---")
    st.markdown("### 🧩 Evaluation Pipeline")
    st.markdown(
        "- 🎓 **Skill & Education** matching\n"
        "- 💼 **Work Experience** alignment\n"
        "- 💰 **Salary** market check\n"
        "- 🧑‍💼 **Supervisor** final decision"
    )
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("Use a structured PDF resume and a clear, complete job description for the best results.")
    st.markdown("---")
    st.caption("Powered by LangChain · Groq · Streamlit")


# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>🧠 AI Resume Analyzer</h1>
    <p>Multi-agent screening for skills, experience, and salary alignment — in seconds.</p>
</div>
""", unsafe_allow_html=True)


# ---------- Inputs ----------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">📄 Upload Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    if resume_file:
        size_kb = round(len(resume_file.getvalue()) / 1024, 1)
        st.success(f"✅ {resume_file.name} uploaded ({size_kb} KB)")

with col2:
    st.markdown('<div class="section-title">📝 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "Job Description",
        height=260,
        placeholder="Paste the full job description here…",
        label_visibility="collapsed",
    )
    if jd_text:
        st.caption(f"📊 {len(jd_text.split())} words · {len(jd_text)} characters")


st.markdown("")
evaluate_btn = st.button("🚀 Evaluate Candidate", disabled=not (resume_file and jd_text))

if not (resume_file and jd_text):
    st.info("ℹ️ Upload a resume PDF **and** paste a job description to enable evaluation.")


# ---------- Evaluation ----------
if evaluate_btn and resume_file and jd_text:
    with st.status("Running multi-agent screening…", expanded=True) as status:
        st.write("📄 Extracting text from resume…")
        resume = extract_text_from_uploaded_pdf(resume_file)

        st.write("🎓 Evaluating skills & education…")
        st.write("💼 Evaluating work experience…")
        st.write("💰 Checking salary alignment…")
        st.write("🧑‍💼 Supervisor making final decision…")

        response = sup_agent.invoke({
            "messages": [
                SystemMessage(content='Return the output in that format only, do not add any other outputs like PERCENTAGE HIKE OR CONFIDENCE.'),
                HumanMessage(content=f"Screen this resume:\n\n{resume}\n\nAgainst this job description:\n\n{jd_text}\n\n"),
            ]
        })
        raw = response["messages"][-1].content
        status.update(label="✅ Evaluation complete", state="complete", expanded=False)

    if not raw:
        st.error("Could not extract model output. Please try again.")
    else:
        parsed = parse_agent_output(raw)

        st.markdown('<div class="section-title">🎯 Screening Result</div>', unsafe_allow_html=True)

        head_c1, head_c2 = st.columns([2, 1])

        with head_c1:
            decision = parsed["decision"]
            if decision in ("ACCEPTED", "APPROVE", "APPROVED"):
                badge_cls, icon = "badge-approve", "✅"
                msg = "This candidate is a strong fit for the role."
            elif decision in ("REJECTED", "REJECT"):
                badge_cls, icon = "badge-reject", "❌"
                msg = "This candidate does not meet key requirements."
            else:
                badge_cls, icon, msg = "badge-reject", "⚠️", "Unable to parse decision."

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="card-title">Final Decision</div>
                    <div style="margin-top:0.4rem;">
                        <span class="badge {badge_cls}">{icon} {decision}</span>
                    </div>
                    <div style="margin-top:0.8rem; color:#4b5563;">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with head_c2:
            score_val = parsed["score"]
            try:
                score_int = int(score_val)
            except (TypeError, ValueError):
                score_int = 0
            st.markdown(
                f"""
                <div class="score-box">
                    <div class="score-label">Overall Score</div>
                    <div class="score-number">{score_val}</div>
                    <div class="score-label">out of 100</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(min(max(score_int, 0), 100) / 100)

        if parsed["summary"]:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="card-title">📋 Candidate Summary</div>
                    <div class="card-value">{parsed["summary"].replace(chr(10), "<br>")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-title">🔍 Detailed Breakdown</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🎓 Skill & Education Fit", "💼 Experience Fit", "💰 Salary Fit"])

        with tab1:
            st.markdown(
                f"""<div class="result-card"><div class="card-value">{parsed["skill_fit"].replace(chr(10), "<br>") or "No data available."}</div></div>""",
                unsafe_allow_html=True,
            )
        with tab2:
            st.markdown(
                f"""<div class="result-card"><div class="card-value">{parsed["experience_fit"].replace(chr(10), "<br>") or "No data available."}</div></div>""",
                unsafe_allow_html=True,
            )
        with tab3:
            st.markdown(
                f"""<div class="result-card"><div class="card-value">{parsed["salary_fit"].replace(chr(10), "<br>") or "No data available."}</div></div>""",
                unsafe_allow_html=True,
            )

        with st.expander("🧾 View Raw Model Output"):
            st.code(raw, language="markdown")

        st.download_button(
            label="⬇️ Download Report",
            data=raw,
            file_name=f"resume_report_{resume_file.name.replace('.pdf','')}.txt",
            mime="text/plain",
        )

try:
    response = sup_agent.invoke({
        "messages": [
            SystemMessage(content='Return the output in that format only...'),
            HumanMessage(content=f"Screen this resume:\n\n{resume}\n\nAgainst this job description:\n\n{jd_text}\n\n"),
        ]
    })
    raw = response["messages"][-1].content
except Exception as e:
    status.update(label="❌ Evaluation failed", state="error", expanded=False)
    st.error(
        "The model failed to orchestrate the evaluation tools correctly. "
        "This usually means the underlying LLM emitted a malformed tool call. "
        "Try again, or switch the supervisor model to `llama-3.3-70b-versatile`."
    )
    with st.expander("🔧 Technical details"):
        st.code(str(e))
    st.stop()