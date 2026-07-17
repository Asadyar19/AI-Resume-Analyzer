import streamlit as st
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🎯",
    layout="wide"
)
from utils.sidebar import render_custom_sidebar
render_custom_sidebar("job_matcher")

from utils.pdf_reader import extract_resume_text
from utils.extractor import extract_skills
from utils.ats import calculate_ats_score

# -----------------------------
# Premium Neon Vibe Custom CSS
# -----------------------------
st.markdown("""
<style>
/* Global Layout Adjustments */
.main > div {
    background-color: #0A0D14;
    padding-top: 1.5rem;
}

h1 {
    text-align: center;
    color: #FFFFFF;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.intro-text {
    text-align: center;
    color: #A0A5B5;
    font-size: 16px;
    margin-bottom: 2.5rem;
}

/* Style Native Column Wrappers as Executive Cards */
div[data-testid="stColumn"] {
    background: linear-gradient(145deg, #111520, #161B26) !important;
    border: 1px solid #222836 !important;
    border-radius: 14px !important;
    padding: 32px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
}

div[data-testid="stColumn"]:hover {
    transform: translateY(-4px) !important;
    border-color: #4CAF50 !important;
    box-shadow: 0 12px 28px rgba(76, 175, 80, 0.22) !important;
}

.section-header {
    font-size: 19px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 1.5rem;
    letter-spacing: -0.3px;
}

/* Centralized Neon Action Button Override */
.button-box {
    display: flex;
    justify-content: center;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}

div.stButton > button {
    background: linear-gradient(135deg, #4CAF50, #45A049) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 45px !important;
    border-radius: 30px !important;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2) !important;
    transition: all 0.25s ease-in-out !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(76, 175, 80, 0.4) !important;
    background: linear-gradient(135deg, #52B756, #4CAF50) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Inner Input Field Custom Blending */
div[data-testid="stTextArea"] textarea {
    background-color: #0E1118 !important;
    border: 1px solid #222836 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 1px #4CAF50 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("<h1>🎯 AI Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown("<p class='intro-text'>Compare your resume text directly against any targeted industry role to pinpoint critical missing keywords and skills optimization steps instantly.</p>", unsafe_allow_html=True)

# -----------------------------
# Input Layout (Clean columns styled dynamically via CSS)
# -----------------------------
input_col1, input_col2 = st.columns([1, 1], gap="large")

with input_col1:
    st.markdown("<div class='section-header'>1. Document Source</div>", unsafe_allow_html=True)
    resume = st.file_uploader(
        "Upload Resume (PDF format only)",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload your latest updated single-page or multi-page career resume document."
    )

with input_col2:
    st.markdown("<div class='section-header'>2. Targeted Role Specification</div>", unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste the Job Description",
        height=130,
        label_visibility="collapsed",
        placeholder="Paste the complete responsibilities, technical keywords, and requirements checklist here...",
        help="Provide the complete target description string from the corporate recruiter posting."
    )

# Centered Core Action Controller
st.markdown('<div class="button-box">', unsafe_allow_html=True)
analyze_btn = st.button("🚀 Analyze Alignment Matrix", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Execution & Analysis Engine Logic Block
# -----------------------------
if analyze_btn:

    if resume is None:
        st.warning("Please upload a resume file to proceed with the comparative keyword match verification calculation step.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste the job description text matrix parameter block before initiating engine assessment.")
        st.stop()

    st.toast("Resume uploaded successfully! ✅")
    resume_text = extract_resume_text(resume)

    with st.spinner("🤖 AI Context Engine processing structural parameters..."):
        data = extract_skills(
            resume_text,
            job_description
        )

    resume_skills = data["resume_skills"]
    job_skills = {
        "required": data["required_skills"],
        "preferred": data["preferred_skills"]
    }

    score, matched, missing = calculate_ats_score(
        resume_skills,
        job_skills
    )

    # Cache calculations into persistent memory
    st.session_state["match_results"] = {
        "score": score,
        "matched": matched,
        "missing": missing,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "resume_text": resume_text
    }

    # Redirect directly to your multi-page layout dashboard file target
    st.switch_page("pages/jdmatcher_report.py")

# -----------------------------
# Footer Component Placement Block
# -----------------------------
st.markdown("<div style='padding-top: 4rem;'></div>", unsafe_allow_html=True)
st.divider()
st.markdown(
    """
    <div style="text-align: center; padding-bottom: 1rem;">
        <p style="color: #6C757D; font-size: 13px; margin: 0;">
            Generated securely via AI Engine
        </p>
        <p style="color: #8C949D; font-size: 13px; font-weight: bold; margin-top: 4px; letter-spacing: 0.5px;">
            System Engineered by M. Asad Yar Khan
        </p>
    </div>
    """,
    unsafe_allow_html=True
)