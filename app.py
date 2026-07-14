import streamlit as st
import pdfplumber

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

        st.subheader("Extracted Resume Text")
        st.text_area(
            "Resume Content",
            resume_text,
            height=400
)