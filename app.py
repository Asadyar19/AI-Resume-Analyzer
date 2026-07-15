import traceback
import streamlit as st

from utils.gemini_client import client
from utils.pdf_reader import extract_resume_text
from utils.prompts import ats_prompt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📄 AI Resume Analyzer")

st.markdown("""
Welcome! 👋

Upload your **Resume (PDF)** and paste a **Job Description**.

Our AI will compare both and provide:

- ✅ ATS Score
- 📊 Skills Match
- ❌ Missing Skills
- 💡 Resume Improvement Suggestions
""")

st.divider()

# -----------------------------
# Resume Upload
# -----------------------------
resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

# -----------------------------
# Job Description
# -----------------------------
job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🚀 Analyze Resume"):

    if resume is None:
        st.warning("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste a job description.")
        st.stop()

    st.success("Resume uploaded successfully!")

    # -----------------------------
    # Extract Resume Text
    # -----------------------------
    resume_text = extract_resume_text(resume)

    # -----------------------------
    # Debug (Remove later if desired)
    # -----------------------------
    with st.expander("📄 Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

    # -----------------------------
    # Generate Prompt
    # -----------------------------
    prompt = ats_prompt(
        resume_text,
        job_description
    )

    # -----------------------------
    # Gemini Analysis
    # -----------------------------
    try:

        with st.spinner("🤖 AI is analyzing your resume..."):

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

        st.subheader("📊 ATS Analysis")
        st.markdown(response.text)

    except Exception:
        st.error("An error occurred while contacting Gemini.")
        st.code(traceback.format_exc())