import streamlit as st

from utils.pdf_reader import extract_resume_text
from utils.extractor import extract_skills
from utils.ats import calculate_ats_score

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

The AI will extract skills from both documents and our ATS engine will calculate:

- ✅ ATS Score
- 📊 Matched Skills
- ❌ Missing Skills
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
# Analyze
# -----------------------------
if st.button("🚀 Analyze Resume"):

    if resume is None:
        st.warning("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.warning("Please paste a job description.")
        st.stop()

    resume_text = extract_resume_text(resume)

    with st.spinner("🤖 Extracting skills..."):

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

    # -----------------------------
    # Results
    # -----------------------------
    st.success("Analysis Complete!")

    st.header("📊 ATS Results")

    st.metric(
        "ATS Score",
        f"{score}%"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("### ✅ Matched Skills")
        st.write(matched)

    with col2:
        st.error("### ❌ Missing Skills")
        st.write(missing)

    # -----------------------------
    # Debug
    # -----------------------------
    with st.expander("🛠 Debug Information"):

        st.subheader("Resume Skills")
        st.json(resume_skills)

        st.subheader("Required Skills")
        st.json(job_skills["required"])

        st.subheader("Preferred Skills")
        st.json(job_skills["preferred"])

        st.subheader("Extracted Resume Text")
        st.text_area(
            "Resume",
            resume_text,
            height=250
        )