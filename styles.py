import streamlit as st


def inject_css():
    """Inject all custom CSS for the Streamlit UI (dark theme)."""
    st.markdown("""
    <style>
        /* ---------- Global ---------- */
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            background-color: #0b1020 !important;
            color: #e5e7eb;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1300px;
        }

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {
            background: #0f1428 !important;
            border-right: 1px solid #1f2544;
        }
        [data-testid="stSidebar"] * {
            color: #d1d5db !important;
        }
        [data-testid="stSidebar"] .stAlert {
            background: #1a2040 !important;
            border: 1px solid #2a3160 !important;
            color: #cbd5e1 !important;
        }

        /* ---------- Hero ---------- */
        .hero {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #9333ea 100%);
            padding: 2rem 2.5rem;
            border-radius: 18px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 40px rgba(124, 58, 237, 0.35);
        }
        .hero h1 { color: white; margin: 0; font-size: 2.2rem; font-weight: 700; }
        .hero p  { color: rgba(255,255,255,0.92); margin-top: 0.4rem; font-size: 1.05rem; }

        /* ---------- Cards ---------- */
        .result-card {
            background: #151a2e;
            border: 1px solid #262c4a;
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 14px rgba(0,0,0,0.35);
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }
        .result-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(124, 58, 237, 0.25);
            border-color: #3b3f72;
        }
        .card-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #9ca3af;
            margin-bottom: 0.6rem;
        }
        .card-value {
            font-size: 1.05rem;
            color: #e5e7eb;
            line-height: 1.55;
        }

        /* ---------- Decision badges ---------- */
        .badge {
            display: inline-block;
            padding: 0.5rem 1.2rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.04em;
        }
        .badge-approve {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid #10b981;
        }
        .badge-reject {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid #ef4444;
        }

        /* ---------- Score box ---------- */
        .score-box {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, #1a1f3a, #2a1f4a);
            border-radius: 14px;
            border: 1px solid #3b3f72;
        }
        .score-number {
            font-size: 3rem;
            font-weight: 800;
            color: #a78bfa;
            line-height: 1;
        }
        .score-label {
            font-size: 0.85rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        /* ---------- File uploader ---------- */
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploaderDropzone"] {
            background: #151a2e !important;
            border: 2px dashed #3b3f72 !important;
            border-radius: 12px !important;
            color: #d1d5db !important;
        }
        [data-testid="stFileUploader"] section * {
            color: #d1d5db !important;
        }
        [data-testid="stFileUploader"] button {
            background: #262c4a !important;
            color: #e5e7eb !important;
            border: 1px solid #3b3f72 !important;
        }

        /* ---------- Text area ---------- */
        textarea, .stTextArea textarea {
            background: #151a2e !important;
            color: #e5e7eb !important;
            border: 1px solid #262c4a !important;
            border-radius: 10px !important;
        }
        textarea::placeholder { color: #6b7280 !important; }

        /* ---------- Buttons ---------- */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            width: 100%;
            transition: transform 0.1s ease, filter 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 4px 14px rgba(139, 92, 246, 0.35);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.1);
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
        }
        .stButton > button:disabled {
            background: #2a2f4a !important;
            color: #6b7280 !important;
            box-shadow: none;
            opacity: 0.6;
        }

        /* ---------- Section title ---------- */
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #e5e7eb;
            margin: 1.5rem 0 0.8rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #262c4a;
        }

        /* ---------- Alerts (info / success / error) ---------- */
        [data-testid="stAlert"] {
            background: #151a2e !important;
            border: 1px solid #262c4a !important;
            color: #d1d5db !important;
            border-radius: 10px;
        }
        [data-testid="stAlert"] * { color: #d1d5db !important; }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] {
            background: transparent;
            border-bottom: 1px solid #262c4a;
            gap: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            background: #151a2e;
            color: #9ca3af;
            border-radius: 10px 10px 0 0;
            padding: 0.6rem 1.2rem;
            border: 1px solid #262c4a;
            border-bottom: none;
        }
        .stTabs [aria-selected="true"] {
            background: #1f2544 !important;
            color: #a78bfa !important;
            border-color: #3b3f72 !important;
        }

        /* ---------- Expander ---------- */
        [data-testid="stExpander"] {
            background: #151a2e;
            border: 1px solid #262c4a;
            border-radius: 10px;
        }
        [data-testid="stExpander"] summary { color: #d1d5db !important; }

        /* ---------- Status box ---------- */
        [data-testid="stStatusWidget"], [data-testid="stStatus"] {
            background: #151a2e !important;
            border: 1px solid #262c4a !important;
            color: #d1d5db !important;
        }

        /* ---------- Progress bar ---------- */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        }

        /* ---------- Code blocks ---------- */
        code, pre, .stCodeBlock {
            background: #0f1428 !important;
            color: #e5e7eb !important;
            border: 1px solid #262c4a !important;
            border-radius: 8px !important;
        }

        /* ---------- Captions ---------- */
        .stCaption, [data-testid="stCaptionContainer"] {
            color: #9ca3af !important;
        }
    </style>
    """, unsafe_allow_html=True)
