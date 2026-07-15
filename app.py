import traceback
import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

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
    resume_text = ""

    with pdfplumber.open(resume) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    resume_text = resume_text.strip()

    # -----------------------------
    # Debug (Can remove later)
    # -----------------------------
    with st.expander("📄 Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

    # -----------------------------
    # Gemini Prompt
    # -----------------------------
    prompt = f"""
You are a senior Technical Recruiter and ATS (Applicant Tracking System) expert.

Analyze the resume against the provided job description.

Base your evaluation ONLY on the information provided.

Do NOT invent skills, experience, certifications, or projects.

Return your response in Markdown using exactly this structure:

# ATS Score
XX/100

# Matched Skills
- Skill 1
- Skill 2
- Skill 3

# Missing Skills
- Skill 1
- Skill 2
- Skill 3

# Resume Improvement Suggestions
1. Suggestion
2. Suggestion
3. Suggestion

Resume:
{resume_text}

Job Description:
{job_description}
"""

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