import streamlit as st
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Analysis Results",
    page_icon="📊",
    layout="wide"
)
from utils.sidebar import render_custom_sidebar
render_custom_sidebar("job_matcher_report")

import html
import plotly.graph_objects as go


# -----------------------------
# Premium UI Theme Custom CSS
# -----------------------------
st.markdown("""
<style>
/* Global Layout Adjustments */
.main > div {
    padding-top: 1.5rem;
    background-color: #0A0D14;
}

/* Centralized Header Typography */
.report-title {
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}

/* Centered Button Wrapper */
.button-box {
    display: flex;
    justify-content: center;
    margin-bottom: 2.5rem;
}

/* Sleek Neon Accent Button Override */
div.stButton > button {
    background: linear-gradient(135deg, #4CAF50, #45A049) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 12px 32px !important;
    border-radius: 30px !important;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2) !important;
    transition: all 0.25s ease-in-out !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
    background: linear-gradient(135deg, #52B756, #4CAF50) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Executive Left-Accent Cards with Hover Effects */
.verdict-card {
    background: linear-gradient(145deg, #111520, #161B26);
    border: 1px solid #222836;
    border-radius: 12px;
    padding: 26px;
    margin-bottom: 2.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease-in-out;
}

.verdict-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(76, 175, 80, 0.15);
}

.verdict-card.success { border-left: 5px solid #4CAF50; }
.verdict-card.info { border-left: 5px solid #2196F3; }
.verdict-card.warning { border-left: 5px solid #00E676; } /* Changed from orange to vibrant green */
.verdict-card.error { border-left: 5px solid #F44336; }

.verdict-header {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #FFFFFF;
}
.verdict-desc {
    color: #A0A5B5;
    font-size: 15px;
    line-height: 1.6;
}

/* Premium KPI Grid System with Hover Shadow Glows */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 1rem;
}

.kpi-card {
    background: linear-gradient(145deg, #121622, #181D2A);
    border: 1px solid #22293A;
    border-radius: 12px;
    padding: 26px 16px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease-in-out;
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: #4CAF50;
    box-shadow: 0 8px 24px rgba(76, 175, 80, 0.25);
}

.kpi-label {
    font-size: 12px;
    font-weight: 700;
    color: #7E8494;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
}

/* Section Header Lines */
.section-header {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 2rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #22293A;
    letter-spacing: -0.2px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State Verification
# -----------------------------
if "match_results" not in st.session_state:
    st.markdown("<div class='report-title'>📊 Profile Alignment Matrix Results</div>", unsafe_allow_html=True)
    
    col_err_l, col_err_c, col_err_r = st.columns([1, 1.2, 1])
    with col_err_c:
        st.markdown('<div class="button-box">', unsafe_allow_html=True)
        if st.button("⬅ Return to Analyzer Core", use_container_width=True):
            st.switch_page("pages/jdmatcher.py")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("""
    <div class="verdict-card warning">
        <div class="verdict-header">⚠️ No Analysis Data Found</div>
        <div class="verdict-desc">Please complete the configuration process and upload your matrix parameters on the main interface before viewing diagnostics.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='padding-top: 4rem;'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
        <div style="text-align: center; padding-bottom: 1rem;">
            <p style="color: #6C757D; font-size: 13px; margin: 0;">Automated evaluation report securely generated via AI Engine</p>
            <p style="color: #8C949D; font-size: 13px; font-weight: bold; margin-top: 4px; letter-spacing: 0.5px;">System Engineered by M. Asad Yar Khan</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Retrieve values
results = st.session_state["match_results"]
score = results["score"]
matched = results["matched"]
missing = results["missing"]
resume_skills = results["resume_skills"]
job_skills = results["job_skills"]
resume_text = results["resume_text"]

# -----------------------------
# UI Component Utilities
# -----------------------------
def skill_badges(skills, bg_color, text_color):
    badges = '<div style="display: flex; flex-wrap: wrap; gap: 10px; padding: 5px 0;">'
    for skill in skills:
        badges += f'<span style="display:inline-block; background:{bg_color}; color:{text_color}; padding:8px 16px; border-radius:30px; font-size:13px; font-weight:600; border:1px solid rgba(255,255,255,0.03);">{html.escape(skill)}</span>'
    badges += "</div>"
    st.markdown(badges, unsafe_allow_html=True)

def create_gauge_chart(score):
    # Updated chart colors to follow the green theme
    gauge_color = "#4CAF50" if score >= 80 else "#2196F3" if score >= 60 else "#00E676" if score >= 40 else "#F44336"
    
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'color': '#FFFFFF', 'size': 58, 'family': 'Helvetica', 'weight': 'bold'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#333", 'tickfont': {'color': '#666'}},
                'bar': {'color': gauge_color, 'thickness': 0.25},
                'bgcolor': "#141923",
                'borderwidth': 0,
                'steps': [{'range': [0, 100], 'color': 'rgba(0,0,0,0)'}]
            }
        )
    )
    
    fig.update_layout(
        height=260,
        margin=dict(l=30, r=30, t=30, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# -----------------------------
# Main Premium Layout
# -----------------------------
st.markdown("<div class='report-title'>📊 Profile Alignment Matrix Results</div>", unsafe_allow_html=True)

# Centered Action Control Pill File Navigation
col_back_l, col_back_c, col_back_r = st.columns([1, 1.2, 1])
with col_back_c:
    st.markdown('<div class="button-box">', unsafe_allow_html=True)
    if st.button("🔄 Match Another Position / Run New Analysis", use_container_width=True):
        st.switch_page("pages/jdmatcher.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Dynamic Strategic Verdict Card Block (Orange states converted to Green)
if score >= 80:
    verdict_class, status_label, info_text = "success", "Verdict: ✅ Excellent Profile Match", "Your core professional competencies and targeted keyword attributes align flawlessly with this target position architecture framework profile spec."
elif score >= 60:
    verdict_class, status_label, info_text = "info", "Verdict: ⚡ Competitive Core Coverage", "Good baseline technical coverage discovered. Injecting the missing keywords highlighted below will significantly strengthen target relevance indices."
elif score >= 40:
    verdict_class, status_label, info_text = "warning", "Verdict: 🟢 Moderate Profile Gaps", "Noticeable keyword variance noticed. We highly recommend incorporating the target domain specifics listed below prior to submitting your formal application."
else:
    verdict_class, status_label, info_text = "error", "Verdict: ❌ Low Alignment Matrix Match", "Significant structural mismatch detected. Comprehensive experience rebranding and targeted technical stack integration required to pass tracking architectures."

st.markdown(f"""
<div class="verdict-card {verdict_class}">
    <div class="verdict-header">{status_label}</div>
    <div class="verdict-desc">{info_text}</div>
</div>
""", unsafe_allow_html=True)

# Dashboard Columns Visualization Metrics Grid Splits
results_left, results_right = st.columns([1.1, 1], gap="large")

with results_left:
    st.markdown("<div class='section-header'>Performance Metrics</div>", unsafe_allow_html=True)
    
    # Custom Grid Design Architecture
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">ATS Index Score</div>
            <div class="kpi-value">{score}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Core Matches</div>
            <div class="kpi-value">{len(matched)}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Deficit Blocks</div>
            <div class="kpi-value">{len(missing)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with results_right:
    st.plotly_chart(
        create_gauge_chart(score),
        use_container_width=True,
        config={"displayModeBar": False}
    )

# Technical Keyword Tag Layout Comparison Layout Split Rows
st.markdown("<div class='section-header'>Granular Keyword Target Comparison</div>", unsafe_allow_html=True)
skills_left, skills_right = st.columns(2, gap="large")

with skills_left:
    st.markdown("### ✅ Verified Skill Coverage")
    if matched:
        skill_badges(matched, "rgba(20, 50, 32, 0.45)", "#4CAF50")
    else:
        st.info("No matching profile keywords parsed during this evaluation calculation run.")

with skills_right:
    st.markdown("### ❌ Identified Critical Deficits")
    if missing:
        skill_badges(missing, "rgba(70, 24, 24, 0.45)", "#FF5252")
    else:
        st.success("Zero keyword deficits parsed! Full target synergy confirmed.")

# Footer Section Injection
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