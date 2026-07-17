import streamlit as st

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

from utils.sidebar import render_custom_sidebar
render_custom_sidebar("Home")

# --------------------------------------------------
# Premium UI Theme Custom CSS
# --------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.main {
    background-color: #0A0D14;
}

/* ---------------- Hero Section ---------------- */
.hero {
    text-align: center;
    padding: 30px 0 50px 0;
    animation: fadeIn 0.8s ease-in-out;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
}

.gradient-text {
    background: linear-gradient(90deg, #FFFFFF, #4CAF50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}          

.hero p {
    color: #A0A5B5;
    font-size: 18px;
    max-width: 740px;
    margin: auto;
    line-height: 1.7;
}

/* ---------------- Navigation Wrappers ---------------- */
a.card-link {
    text-decoration: none !important;
    color: inherit !important;
    display: block;
}

/* ---------------- Interactive Tool Cards ---------------- */
.tool-card {
    background: linear-gradient(145deg, #111520, #161B26);
    border: 1px solid #222836;
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.3s ease-in-out;
    height: 520px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.tool-card:hover {
    transform: translateY(-6px);
    border-color: #4CAF50;
    box-shadow: 0 12px 30px rgba(76, 175, 80, 0.2);
}

/* Accent Header Bars */
.neon-green-bar {
    height: 5px;
    background: linear-gradient(90deg, #4CAF50, #6DFF7B);
}

.neon-blue-bar {
    height: 5px;
    background: linear-gradient(90deg, #00BCD4, #2979FF);
}

.card-content {
    padding: 32px;
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 30px;
    background: rgba(255, 255, 255, 0.04);
    color: #4CAF50;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 18px;
    border: 1px solid rgba(255, 255, 255, 0.02);
}

.icon {
    font-size: 64px;
    text-align: center;
    margin-top: 5px;
}

.card-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 10px;
}

.card-subtitle {
    text-align: center;
    color: #A0A5B5;
    margin-top: 10px;
    margin-bottom: 25px;
    line-height: 1.6;
    font-size: 15px;
}

/* Feature Checklists */
.feature {
    display: flex;
    align-items: center;
    margin: 12px 0;
    font-size: 15px;
    color: #E2E4E9;
}

.feature span {
    margin-right: 12px;
    font-size: 18px;
}

/* Layout Section Titles */
.section-title {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 60px 0 30px 0;
    letter-spacing: -0.2px;
}

/* ---------------- Info & Value Cards ---------------- */
.info-card {
    background: linear-gradient(145deg, #111520, #161B26);
    border: 1px solid #222836;
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    min-height: 250px;
}

.info-card:hover {
    transform: translateY(-4px);
    border-color: #4CAF50;
    box-shadow: 0 10px 24px rgba(76, 175, 80, 0.15);
}

.info-icon {
    font-size: 38px;
    margin-bottom: 14px;
}

.info-title {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 10px;
}

.info-text {
    color: #A0A5B5;
    font-size: 14px;
    line-height: 1.6;
}

/* ---------------- Rebuilt KPI Matrix Grid ---------------- */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 1rem;
}

.stats-card {
    background: linear-gradient(145deg, #111520, #161B26);
    border: 1px solid #222836;
    border-radius: 12px;
    padding: 24px 16px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
}

.stats-card:hover {
    transform: translateY(-4px);
    border-color: #4CAF50;
    box-shadow: 0 8px 24px rgba(76, 175, 80, 0.2);
}

.stats-label {
    font-size: 11px;
    font-weight: 700;
    color: #7E8494;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.stats-value {
    font-size: 30px;
    font-weight: 800;
    color: #FFFFFF;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🚀 <span class="gradient-text">AI Resume Intelligence Platform</span></h1>
    <p>
        Build stronger resumes with cutting-edge analytical models. 
        Analyze structural ATS compatibility, interpret recruiter intent profiles, 
        and pinpoint critical technical skill deficits instantly—all from a unified control dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CORE SYSTEM PORTALS
# --------------------------------------------------
left, right = st.columns(2, gap="large")

with left:
    st.markdown("""
    <a href="resume_auditor" class="card-link" target="_self">
        <div class="tool-card">
            <div class="neon-green-bar"></div>
            <div class="card-content">
                <div class="badge">🤖 AI RESUME AUDIT</div>
                <div class="icon">📄</div>
                <div class="card-title">Resume Auditor</div>
                <div class="card-subtitle">
                    Evaluate your resume tracking mechanics using an operational AI engine to extract comprehensive stylistic diagnostic reports.
                </div>
                <div class="feature"><span>✅</span>ATS Readiness Scoring Index</div>
                <div class="feature"><span>📊</span>Structural Layout Variance Quality Check</div>
                <div class="feature"><span>👀</span>Recruiter First Impression Modeling</div>
                <div class="feature"><span>📑</span>Critical Core Missing Section Extraction</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <a href="jdmatcher" class="card-link" target="_self">
        <div class="tool-card">
            <div class="neon-blue-bar"></div>
            <div class="card-content">
                <div class="badge">🎯 SMART JOB MATCHING</div>
                <div class="icon">🎯</div>
                <div class="card-title">Resume vs Job Matcher</div>
                <div class="card-subtitle">
                    Map out professional keyword coverage profiles directly against targeted corporate requirements descriptions to resolve missing components.
                </div>
                <div class="feature"><span>📈</span>ATS Alignment Match Score Matrix</div>
                <div class="feature"><span>🛠️</span>Granular Operational Skill Gap Mapping</div>
                <div class="feature"><span>❌</span>Immediate Deficit Keyword Highlights</div>
                <div class="feature"><span>💼</span>Hiring Profile Synergy Analytics</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# PLATFORM VALUES & ARCHITECTURE
# --------------------------------------------------
st.markdown("<div class='section-title'>✨ Platform Architecture Strategy</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🤖</div>
        <div class="info-title">Advanced Gemini AI</div>
        <div class="info-text">
            Utilizes complex semantic processing layers to interpret overall career layout contexts rather than basic phrase counting mechanics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">⚡</div>
        <div class="info-title">Lightning Metrics</div>
        <div class="info-text">
            Compiles dense cross-verification tracking points, layout validations, and full alignment statistics inside an isolated sub-10 second loop.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">📈</div>
        <div class="info-title">ATS Matrix Optimization</div>
        <div class="info-text">
            Engineered precisely around underlying schema models utilized across modern enterprise corporate applicant screening pipelines.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# METRICS PERFORMANCE HIGHLIGHTS
# --------------------------------------------------
st.markdown("<div class='section-title'>📊 Platform Operational Highlights</div>", unsafe_allow_html=True)

st.markdown("""
<div class="stats-grid">
    <div class="stats-card">
        <div class="stats-label">Core Engine</div>
        <div class="stats-value">Gemini</div>
    </div>
    <div class="stats-card">
        <div class="stats-label">Diagnostics</div>
        <div class="stats-value">Real-Time</div>
    </div>
    <div class="stats-card">
        <div class="stats-label">ATS Framework</div>
        <div class="stats-value">Modern</div>
    </div>
    <div class="stats-card">
        <div class="stats-label">Latency Index</div>
        <div class="stats-value">&lt; 10s</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BRAND FOOTER
# --------------------------------------------------
st.markdown("<div style='padding-top: 4rem;'></div>", unsafe_allow_html=True)
st.divider()
st.markdown(
    """
    <div style="text-align: center; padding-bottom: 1rem;">
        <p style="color: #6C757D; font-size: 13px; margin: 0;">
            Automated evaluation infrastructure securely hosted via AI Engine
        </p>
        <p style="color: #8C949D; font-size: 13px; font-weight: bold; margin-top: 5px; letter-spacing: 0.5px;">
            System Engineered by M. Asad Yar Khan
        </p>
    </div>
    """,
    unsafe_allow_html=True
)