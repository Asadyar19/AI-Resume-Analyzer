import streamlit as st
# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Resume Auditor",
    page_icon="📄",
    layout="wide"
)

from utils.sidebar import render_custom_sidebar
render_custom_sidebar("Auditor")

import pdfplumber
import time
from utils.pdf_reader import extract_resume_text
from utils.resume_audit import audit_resume



# -------------------------------------------------
# Custom CSS for Upload Page
# -------------------------------------------------
st.markdown("""
<style>
/* 1. Ambient Background Glow */
.stApp {
    background: radial-gradient(circle at 25% 25%, rgba(76, 175, 80, 0.05) 0%, #0E1117 50%) !important;
}

.block-container {
    max-width: 1050px;
    padding-top: 4rem;
}

/* 2. Target the ENTIRE Left Streamlit Column and turn it into a Card */
[data-testid="column"]:nth-of-type(1) {
    background: #171A21;
    border: 1px solid #2D3342;
    border-top: 4px solid #4CAF50;
    border-radius: 16px;
    padding: 35px 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* Align the Right Column */
[data-testid="column"]:nth-of-type(2) {
    padding-top: 5px;
}

/* 3. Deepen the Dropzone */
[data-testid="stFileUploadDropzone"] {
    background-color: #1E222B !important;
    border: 2px dashed #3A4150 !important;
    border-radius: 12px !important;
    padding: 40px 20px !important;
    transition: all 0.3s ease !important;
    margin-bottom: 5px !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #4CAF50 !important;
    background-color: rgba(76, 175, 80, 0.05) !important;
}

/* 4. Annihilate Streamlit's Default Salmon Button */
button[kind="primary"] {
    background: linear-gradient(90deg, #4CAF50, #2E7D32) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 52px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    margin-top: 15px !important;
    width: 100% !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3) !important;
}

/* Right-Side Panel Styling */
.instruction-card {
    background: #171A21;
    border: 1px solid #2D3342;
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    height: 100%;
}

.instruction-step {
    display: flex;
    align-items: flex-start;
    margin-bottom: 24px;
}

.step-icon {
    background: rgba(76, 175, 80, 0.1);
    color: #4CAF50;
    border: 1px solid #4CAF50;
    border-radius: 8px;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
    margin-right: 18px;
    flex-shrink: 0;
}

.step-text h4 {
    margin: 0 0 6px 0;
    color: #E0E0E0;
    font-size: 16px;
    font-weight: 600;
}

.step-text p {
    margin: 0;
    color: #8F8F8F;
    font-size: 14px;
    line-height: 1.6;
}

/* Typography Enhancements */
.gradient-text {
    background: linear-gradient(90deg, #ffffff, #4CAF50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Asymmetrical Layout Split
# -------------------------------------------------
left_col, right_col = st.columns([1.1, 1], gap="large")

# ==========================================
# LEFT COLUMN: THE ACTION ZONE
# ==========================================
with left_col:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 36px; margin-bottom: 8px; font-weight: 800;">📄 <span class="gradient-text">Upload Resume</span></h1>
        <p style="color: #A0AAB5; font-size: 15.5px; line-height: 1.6;">
            Deploy our AI engine to simulate a technical recruiter's ATS screening process instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], label_visibility="hidden")

    if st.button("🚀 Audit Resume", type="primary", width="stretch"):
        if resume is None:
            st.warning("Please upload a resume to proceed.")
            st.stop()

        with st.status("🤖 Initializing AI System...", expanded=True) as status:
            st.write("Extracting document structure and text data...")
            time.sleep(0.5) 
            
            resume_text = extract_resume_text(resume)
            resume.seek(0)
            with pdfplumber.open(resume) as pdf:
                page_count = len(pdf.pages)
            resume.seek(0)

            st.write("Calculating spatial layout and key metrics...")
            time.sleep(0.5)
            
            word_count = len(resume_text.split())
            char_count = len(resume_text)
            reading_time = max(1, round(word_count / 200))
            bullet_count = (resume_text.count("•") + resume_text.count("-") + resume_text.count("▪"))

            if page_count == 1:
                length_status = "✅ Ideal"
            elif page_count == 2:
                length_status = "🟡 Acceptable"
            else:
                length_status = "🔴 Too Long"

            st.write("Evaluating against ATS algorithms and recruiter models...")
            audit = audit_resume(resume_text)
            
            status.update(label="Audit Complete! Rerouting to dashboard...", state="complete", expanded=False)

        st.session_state["audit_data"] = {
            "audit": audit,
            "resume_text": resume_text,
            "page_count": page_count,
            "word_count": word_count,
            "char_count": char_count,
            "reading_time": reading_time,
            "bullet_count": bullet_count,
            "length_status": length_status
        }
        
        st.switch_page("pages/resume_report.py")

    st.markdown("""
    <div style="display:flex; justify-content:center; gap:20px; margin-top:20px; color:#5C6573; font-size:12.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
        <span>🔒 100% Private</span>
        <span>•</span>
        <span>📄 PDF Only</span>
        <span>•</span>
        <span>⚡ Gemini AI</span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# RIGHT COLUMN: VALUE PROP PANEL
# ==========================================
with right_col:
    st.markdown("""
<div class="instruction-card">
<h3 style="margin-top:0; margin-bottom:25px; font-size:20px; border-bottom:1px solid #2D3342; padding-bottom:15px; color:white;">
🔍 What the AI Scans For
</h3>

<div class="instruction-step">
<div class="step-icon">1</div>
<div class="step-text">
<h4>ATS Parsing Simulation</h4>
<p>Tests if standard Applicant Tracking Systems can extract your text without formatting corruption.</p>
</div>
</div>

<div class="instruction-step">
<div class="step-icon">2</div>
<div class="step-text">
<h4>Semantic Keyword Mapping</h4>
<p>Identifies hard skills, high-impact action verbs, and industry-specific terminology.</p>
</div>
</div>

<div class="instruction-step">
<div class="step-icon">3</div>
<div class="step-text">
<h4>Structural Integrity Check</h4>
<p>Validates the presence and order of essential sections like Education, Experience, and Skills.</p>
</div>
</div>

<div class="instruction-step" style="margin-bottom:0;">
<div class="step-icon">4</div>
<div class="step-text">
<h4>Recruiter's First Impression</h4>
<p>Generates actionable feedback mimicking a technical recruiter's 6-second visual scan.</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.markdown(
    """
    <div style="text-align: center;">
        <p style="color: gray; font-size: 14px;">
            System Designed by M. Asad Yar Khan ❤️ using Streamlit, Google Gemini, and Python.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)