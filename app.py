import traceback

import streamlit as st
import pdfplumber
import os
from dotenv import load_dotenv
from google import genai
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

    elif job_description.strip() == "":
        st.warning("Please paste a job description.")

    else:
        st.success("Resume uploaded successfully!")

        resume_text = ""

        with pdfplumber.open(resume) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                   resume_text += text + "\n"
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents="Say hello in one sentence."
        )
            st.subheader("Gemini Response")
            st.write(response.text)
        
        except Exception as e:
            st.error(str(e))
            st.code(traceback.format_exc())    
