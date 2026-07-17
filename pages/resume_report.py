import streamlit as st
# -------------------------------------------------
# Page Config & State Check
# -------------------------------------------------
st.set_page_config(page_title="Resume Audit Report", page_icon="📊", layout="wide")
from utils.sidebar import render_custom_sidebar
render_custom_sidebar("Audit_report")
import plotly.graph_objects as go
from utils.gemini_client import client
from utils.pdf_generator import generate_audit_pdf
from collections import Counter
import re

# -------------------------------------------------
# 🔒 Session State Check & Empty State UI
# -------------------------------------------------
if "audit_data" not in st.session_state:
    
    # Inject the premium neon CSS before the page stops
    st.markdown("""
    <style>
    /* Neon Glassmorphism Card */
    .neon-card {
        background: rgba(23, 26, 33, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(76, 175, 80, 0.2);
        border-top: 4px solid #4CAF50;
        border-radius: 12px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(76, 175, 80, 0.15), inset 0 0 20px rgba(76, 175, 80, 0.05);
        transition: all 0.3s ease;
    }
    .neon-card:hover {
        box-shadow: 0 0 40px rgba(76, 175, 80, 0.25), inset 0 0 20px rgba(76, 175, 80, 0.1);
        border: 1px solid rgba(76, 175, 80, 0.4);
    }
    
    /* Glowing Icon */
    .neon-icon {
        font-size: 45px;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 12px rgba(76, 175, 80, 0.6));
    }

    /* Premium Button CSS */
    button[kind="primary"] {
        background: linear-gradient(90deg, #4CAF50, #2E7D32) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2) !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Push it down to the center of the screen
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # Use columns to perfectly center the empty state card
    spacer1, center_col, spacer2 = st.columns([1, 1.5, 1])
    
    with center_col:
        st.markdown("""
        <div class="neon-card">
            <div class="neon-icon">⚡</div>
            <h3 style="color:white; margin-top:0; margin-bottom:10px; font-weight:700; letter-spacing:1px;">NO DATA DETECTED</h3>
            <p style="color:#A0AAB5; font-size:15px; margin-bottom:0; line-height:1.6;">System memory is currently empty. Please initialize a new session by uploading your document to the analyzer.</p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        # Center the button under the card
        if st.button("⬅️ Initialize Upload Hub", type="primary", width="stretch"):
            st.switch_page("pages/resume_auditor.py") 
            
    st.stop() # Halts the rest of the page

data = st.session_state["audit_data"]
audit = data["audit"]
score = audit["ats_score"]

# -------------------------------------------------
# CSS Architecture & Animations
# -------------------------------------------------
st.markdown("""
<style>
/* Ambient Background */
.stApp {
    background: radial-gradient(circle at 50% 0%, rgba(76, 175, 80, 0.03) 0%, #0E1117 60%) !important;
}

.main > div{ padding-top:2rem; }
h1{ text-align:center; margin-bottom: 40px;}

/* Cascading Animations */
@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-1 { animation: slideUpFade 0.6s ease-out forwards; }
.animate-2 { animation: slideUpFade 0.6s ease-out 0.15s forwards; opacity: 0; }
.animate-3 { animation: slideUpFade 0.6s ease-out 0.3s forwards; opacity: 0; }

/* Apply animations to Streamlit native elements */
[data-testid="stPlotlyChart"] {
    animation: slideUpFade 0.6s ease-out 0.25s forwards;
    opacity: 0;
}

/* Glassmorphism Metric Cards */
.glass-metric {
    background: #171A21;
    border: 1px solid #2D3342;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease;
    box-shadow: 0 6px 14px rgba(0,0,0,0.15);
    height: 100%;
}
.glass-metric:hover {
    border-color: #4CAF50;
    transform: translateY(-5px);
}
.metric-icon { font-size: 32px; margin-bottom: 12px; }
.metric-label { color: #8F8F8F; font-size: 13px; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; font-weight: 600;}
.metric-value { color: white; font-size: 26px; font-weight: 800; }

/* Ruthless Expander Overrides */
[data-testid="stExpander"] {
    background-color: #171A21 !important;
    border: 1px solid #2D3342 !important;
    border-radius: 12px !important;
    transition: all 0.3s ease;
    animation: slideUpFade 0.6s ease-out 0.35s forwards;
    opacity: 0;
}
[data-testid="stExpander"]:hover {
    border-color: #4CAF50 !important;
}
[data-testid="stExpander"] summary p {
    font-weight: 700 !important;
    font-size: 16px !important;
    color: #E0E0E0 !important;
}
[data-testid="stExpanderDetails"] {
    background-color: #1E222B !important;
    border-top: 1px solid #2D3342 !important;
    padding: 15px !important;
}
/* Ruthless Button Overrides */
button[kind="primary"] {
    background: linear-gradient(90deg, #4CAF50, #2E7D32) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3) !important;
}

button[kind="secondary"] {
    background: #1E222B !important;
    color: #E0E0E0 !important;
    border: 1px solid #3A4150 !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

button[kind="secondary"]:hover {
    border-color: #4CAF50 !important;
    color: white !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Helper UI Functions
# -------------------------------------------------
def render_glass_metric(icon, label, value, animation_class="animate-2"):
    st.markdown(f"""
    <div class="glass-metric {animation_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def ats_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix":"%", "font":{"size":46, "color": "white", "family": "'Segoe UI', sans-serif"}},
        gauge={
            "axis":{"range":[0,100], "tickwidth": 1, "tickcolor": "#555"},
            "bar":{"color":"#4CAF50"},
            "bgcolor": "#171A21",
            "borderwidth": 2,
            "bordercolor": "#2D3342",
            "steps":[
                {"range":[0,40], "color":"rgba(229, 57, 53, 0.2)"},
                {"range":[40,70], "color":"rgba(251, 140, 0, 0.2)"},
                {"range":[70,100], "color":"rgba(76, 175, 80, 0.2)"}
            ]
        }
    ))
    fig.update_layout(height=280, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white", family="'Segoe UI', sans-serif"))
    return fig

def resume_radar(scores):
    categories = ["Formatting", "Readability", "Keywords", "Bullets", "Action Verbs", "Achievements"]
    values = [
        scores["formatting"], scores["readability"], scores["keyword_density"],
        scores["bullet_points"], scores["action_verbs"], scores["quantified_achievements"]
    ]
    values += [values[0]]
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values, theta=categories, fill="toself",
        line=dict(color="#00BCD4", width=3), fillcolor="rgba(0, 188, 212, 0.25)"
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white", family="'Segoe UI', sans-serif"),
        polar=dict(
            bgcolor="#171A21",
            radialaxis=dict(visible=True, range=[0,100], gridcolor="#333", linecolor="#333"),
            angularaxis=dict(gridcolor="#333", linecolor="#333")
        ),
        showlegend=False, height=360, margin=dict(l=30,r=30,t=30,b=30)
    )
    return fig

def resume_grade(score):
    if score >= 95: return "A+"
    elif score >= 90: return "A"
    elif score >= 85: return "B+"
    elif score >= 80: return "B"
    elif score >= 75: return "C+"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    return "F"

def overall_verdict(score):
    if score >= 90: return ("🏆 Excellent", "#2E7D32", "Highly ATS optimized and ready for top-tier applications.")
    elif score >= 80: return ("✅ Strong", "#43A047", "Competitive layout. Minor keyword adjustments will make it outstanding.")
    elif score >= 70: return ("⚡ Good", "#FB8C00", "Solid foundation, but structural improvements are required.")
    elif score >= 60: return ("⚠ Needs Work", "#F4511E", "May struggle to pass strict Applicant Tracking Systems.")
    else: return ("❌ Major Rewrite", "#E53935", "Requires significant structural and content optimization.")

def info_cards(title, items, color):
    # Start the HTML block (Flush left to prevent code block rendering)
    html_content = f"""
<div class="animate-3" style="border-left:5px solid {color}; border-radius:12px; background:#1E222B; padding:22px; margin-bottom:15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
<h3 style="color:{color};margin-top:0;font-size:20px;margin-bottom:15px;">{title}</h3>
"""
    
    # Append each item as a styled HTML row inside the div
    for item in items:
        html_content += f"""
<div style="background: rgba(76, 175, 80, 0.1); border: 1px solid rgba(76, 175, 80, 0.2); padding: 12px 15px; margin-bottom: 10px; border-radius: 8px; color: #E0E0E0; font-size: 14.5px;">
<span style="color: #4CAF50; font-weight: 800;">✓</span> <span style="margin-left: 8px;">{item}</span>
</div>
"""
        
    # Close the div and render it ALL AT ONCE
    html_content += "</div>"
    st.markdown(html_content, unsafe_allow_html=True)

def priority_card(title, priority, gain, color):
    st.markdown(f"""
    <div class="animate-3" style="background:#1E222B; border:1px solid #30363d; border-top:6px solid {color}; border-radius:14px; padding:20px; min-height:160px; box-shadow:0 6px 14px rgba(0,0,0,.18);">
    <div style="color:{color}; font-weight:800; font-size:16px; letter-spacing:0.5px; margin-bottom:12px;">{priority}</div>
    <div style="font-size:26px; font-weight:800; color:white; margin-bottom:18px;">+{gain} ATS</div>
    <div style="color:#b8c1cc; font-size:14px;">Estimated Improvement</div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("💡 View Recommendation"):
        st.write(title)

def recruiter_view(audit):
    strengths = audit["strengths"][:3]
    weaknesses = audit["weaknesses"][:3]
    html = """
    <div class="animate-2" style="border:1px solid #2D3342; border-radius:16px; padding:30px; margin-top:10px; margin-bottom:10px; background: linear-gradient(145deg, #1A1D24 0%, #171A21 100%); box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
    <h2 style="margin-top:0; font-size:24px;">👀 Recruiter's 15-Second Glance</h2>
    <p style="color:#8F8F8F; font-size:15px;">What an experienced technical recruiter immediately notices during an initial screen.</p>
    <div style="display:flex; gap:35px; margin-top:25px;">
    <div style="flex:1;"><h3 style="color:#4CAF50; font-size:18px; margin-bottom:15px;">✓ Hiring Strengths</h3><ul style="color:#E0E0E0;">
    """
    for item in strengths: html += f"<li style='margin-bottom:14px; line-height:1.5;'>{item}</li>"
    html += "</ul></div><div style='flex:1;'><h3 style='color:#FF9800; font-size:18px; margin-bottom:15px;'>⚠ Potential Red Flags</h3><ul style='color:#E0E0E0;'>"
    for item in weaknesses: html += f"<li style='margin-bottom:14px; line-height:1.5;'>{item}</li>"
    html += "</ul></div></div></div>"
    st.markdown(html, unsafe_allow_html=True)

def missing_sections_card(audit):
    recommendations = {
        "contact_information": {
            "why": "Recruiters and ATS systems need clear contact details so employers can easily reach you.",
            "include": [
                "Full Name",
                "Professional Email",
                "Phone Number",
                "LinkedIn Profile",
                "Portfolio/Website (if applicable)"
            ]
        },
        "professional_summary": {
            "why": "A concise summary quickly introduces your background and strongest qualifications.",
            "include": [
                "2–4 sentence professional summary",
                "Years of experience",
                "Core strengths",
                "Career objective"
            ]
        },
        "education": {
            "why": "Education is one of the first sections recruiters look for, especially for students and graduates.",
            "include": [
                "Degree",
                "Institution",
                "Graduation Year",
                "Relevant coursework (optional)",
                "GPA (optional)"
            ]
        },
        "experience": {
            "why": "Work experience demonstrates your practical abilities and professional impact.",
            "include": [
                "Job Title",
                "Company",
                "Employment Dates",
                "Responsibilities",
                "Measurable achievements"
            ]
        },
        "projects": {
            "why": "Projects showcase practical experience, especially if professional experience is limited.",
            "include": [
                "Project Title",
                "Brief description",
                "Your contribution",
                "Results or impact"
            ]
        },
        "skills": {
            "why": "Skills help recruiters and ATS quickly identify your qualifications.",
            "include": [
                "Technical skills",
                "Professional skills",
                "Relevant software/tools",
                "Soft skills"
            ]
        },
        "certifications": {
            "why": "Certifications validate your expertise and demonstrate continuous learning.",
            "include": [
                "Professional certifications",
                "Industry licenses",
                "Completed training programs",
                "Online certifications"
            ]
        },
        "achievements": {
            "why": "Achievements distinguish you from other candidates by highlighting exceptional accomplishments.",
            "include": [
                "Awards",
                "Scholarships",
                "Competitions",
                "Special recognitions"
            ]
        },
        "languages": {
            "why": "Knowing multiple languages can be a valuable advantage in many careers.",
            "include": [
                "Languages spoken",
                "Proficiency level"
            ]
        },
        "volunteer_experience": {
            "why": "Volunteer work demonstrates leadership, teamwork and community involvement.",
            "include": [
                "Organization",
                "Role",
                "Dates",
                "Contributions"
            ]
        },
        "publications": {
            "why": "Publications strengthen resumes in research, academia and specialized industries.",
            "include": [
                "Research papers",
                "Articles",
                "Books",
                "Conference publications"
            ]
        },
        "awards": {
            "why": "Awards provide third-party recognition of your achievements and excellence.",
            "include": [
                "Academic awards",
                "Professional awards",
                "Industry recognition"
            ]
        }
    }

    missing = [section for section, exists in audit["sections"].items() if not exists]

    if not missing:
        st.markdown("""<div class="animate-3" style="background:rgba(76, 175, 80, 0.1); border-left:4px solid #4CAF50; padding:16px; border-radius:8px; color:#E0E0E0; font-size:16px;">🎉 <b>Structural Integrity: Excellent.</b> All core ATS sections detected.</div>""", unsafe_allow_html=True)
        return

    st.markdown("<h3 class='animate-3' style='margin-top:0;'>📂 Missing ATS Sections</h3>", unsafe_allow_html=True)
    st.markdown("<p class='animate-3' style='color:#8F8F8F; font-size:15px; margin-bottom:15px;'>Adding these sections can improve both ATS compatibility and recruiter appeal.</p>", unsafe_allow_html=True)

    for section in missing:
        info = recommendations.get(section)
        title = section.replace("_", " ").title()

        with st.expander(f"❌ {title}", expanded=False):
            if info:
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <div style="color: #4CAF50; font-weight: 700; font-size: 15px; margin-bottom: 6px;">💡 Why it matters</div>
                    <div style="background: rgba(255,255,255,0.03); border-left: 3px solid #00BCD4; padding: 12px 15px; border-radius: 0 6px 6px 0; color: #E0E0E0; font-size: 14.5px; line-height: 1.5;">
                        {info['why']}
                    </div>
                </div>
                <div style="color: #4CAF50; font-weight: 700; font-size: 15px; margin-bottom: 10px;">🎯 What to include</div>
                """, unsafe_allow_html=True)

                for item in info["include"]:
                    st.markdown(f"""
                    <div style='color: #B8B8B8; font-size: 14.5px; margin-bottom: 6px; display: flex; align-items: center;'>
                        <span style='color: #4CAF50; margin-right: 10px; font-size: 10px;'>■</span> {item}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #B8B8B8; font-size: 14.5px;'>Consider adding this section if it is relevant to your career.</div>", unsafe_allow_html=True)

def keyword_chart(text):
    stop_words = {"the","and","for","with","from","that","this","your","have","has","had","are","was","were","will","using","into","their","them","than","also","can","our","you","all","not","but","its","his","her","she","him","they","been","being","over","under","after","before","while","through","within","each","more","less","very","able","work","worked","working","resume","experience"}
    words = re.findall(r"\b[a-zA-Z][a-zA-Z+#.]{2,}\b", text.lower())
    words = [w for w in words if w not in stop_words]
    counts = Counter(words)
    top = counts.most_common(10)
    
    if not top:
        return go.Figure()

    labels = [x[0].title() for x in top]
    values = [x[1] for x in top]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h", text=values, textposition="outside",
        marker=dict(color=values, colorscale="Tealgrn")
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white", family="'Segoe UI', sans-serif"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(autorange="reversed", gridcolor="#333"),
        margin=dict(l=10, r=30, t=10, b=10), height=380
    )
    return fig

# -------------------------------------------------
# Render Dashboard
# -------------------------------------------------
st.markdown("<h1 class='animate-1'>📊 ATS Intelligence Report</h1>", unsafe_allow_html=True)
# -------------------------------------------------

# THE FIX: We pass the exact 'audit' variable that your UI is already using!
pdf_bytes = generate_audit_pdf(audit)

# Top Action Bar (Centered)
spacer_left, btn_col1, btn_col2, spacer_right = st.columns([1.5, 1, 1, 1.5])

with btn_col1:
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="ATS_Intelligence_Report.pdf",
        mime="application/pdf",
        width="stretch"
    )

with btn_col2:
    if st.button("🔄 Audit Another Resume", type="primary", width="stretch"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/resume_auditor.py")

st.markdown("<br>", unsafe_allow_html=True)

# Top Verdict Banner (Unified Flexbox Layout)
grade = resume_grade(score)
status, color, verdict = overall_verdict(score)
st.markdown(f"""
<div class="animate-1" style="display:flex; align-items:center; background: linear-gradient(135deg, #171A21 0%, #0E1117 100%); border:1px solid #2D3342; padding:35px; border-radius:20px; border-left:8px solid {color}; margin-bottom:30px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
    <div style="flex:1.5;">
        <h2 style="margin-top:0; font-size:32px; font-weight:800; margin-bottom:8px;">Verdict: {status}</h2>
        <h3 style="color:#B8B8B8; font-size:20px; margin-top:0; font-weight:500;">Grade: <span style="color:white; font-weight:800;">{grade}</span></h3>
        <p style="font-size:17px; color:#A0AAB5; line-height:1.6; margin-top:15px; max-width:90%;">{verdict}</p>
    </div>
    <div style="flex:1; display:flex; justify-content:center;">
""", unsafe_allow_html=True)
st.plotly_chart(ats_gauge(score), width="stretch", config={"displayModeBar": False})
st.markdown("</div></div>", unsafe_allow_html=True)

# Top Glass Metrics Row
c1, c2, c3 = st.columns(3)
with c1: render_glass_metric("📈", "ATS Compatibility Score", f"{score}%", "animate-2")
with c2: render_glass_metric("👁️", "Readability Score", f"{audit['scores']['readability']}/100", "animate-2")
with c3: render_glass_metric("🎯", "Keyword Density", f"{audit['scores']['keyword_density']}/100", "animate-2")

st.markdown("<br>", unsafe_allow_html=True)

# Middle Row: Radar & Checklist
bottom_left, bottom_right = st.columns([1.5, 1], gap="large")
with bottom_left:
    st.markdown("<h3 class='animate-2' style='margin-top:0;'>🕸️ Structural Analysis Radar</h3>", unsafe_allow_html=True)
    st.plotly_chart(resume_radar(audit["scores"]), width="stretch", config={"displayModeBar": False})
with bottom_right:
    st.markdown("<h3 class='animate-2' style='margin-top:0;'>📋 Section Validation</h3>", unsafe_allow_html=True)
    
    # Open the wrapper div as a string
    validation_html = "<div class='animate-2' style='margin-top: 15px;'>"
    
    # Append the results to the string
    for key, value in audit["sections"].items():
        title = key.replace("_", " ").title()
        if value:
            validation_html += f"""<div style="background:rgba(76, 175, 80, 0.1); border-left:4px solid #4CAF50; padding:12px 15px; margin-bottom:10px; border-radius:6px; color:#E0E0E0; font-size:15px;">✅ <span style="margin-left:8px; font-weight:600;">{title}</span></div>"""
        else:
            validation_html += f"""<div style="background:rgba(229, 57, 53, 0.1); border-left:4px solid #E53935; padding:12px 15px; margin-bottom:10px; border-radius:6px; color:#E0E0E0; font-size:15px;">❌ <span style="margin-left:8px; font-weight:600;">{title}</span></div>"""
            
    # Close the wrapper div and render
    validation_html += "</div>"
    st.markdown(validation_html, unsafe_allow_html=True)

st.divider()

# Secondary Glass Metrics Row (Stats)
st.markdown("<h3 class='animate-3' style='margin-top:0;'>📄 Resume Statistics</h3>", unsafe_allow_html=True)
s1, s2, s3, s4, s5 = st.columns(5)
with s1: render_glass_metric("📑", "Pages", data["page_count"], "animate-3")
with s2: render_glass_metric("📝", "Words", data["word_count"], "animate-3")
with s3: render_glass_metric("🔤", "Characters", data["char_count"], "animate-3")
with s4: render_glass_metric("•", "Bullets", data["bullet_count"], "animate-3")
with s5: render_glass_metric("⏳", "Length", data["length_status"], "animate-3")

st.divider()

# Keywords & Recruiter View
col_kw, col_rec = st.columns([1, 1.2], gap="large")
with col_kw:
    st.markdown("<h3 class='animate-3' style='margin-top:0;'>🔑 Keyword Density Map</h3>", unsafe_allow_html=True)
    st.plotly_chart(keyword_chart(data["resume_text"]), width="stretch", config={"displayModeBar": False})
with col_rec:
    recruiter_view(audit)

st.divider()
missing_sections_card(audit)
st.divider()

# Strengths and Roadmaps
left, right = st.columns([1,1.5], gap="large")
with left:
    info_cards("💪 Core Strengths", audit["strengths"], "#4CAF50")
with right:
    st.markdown("<h3 class='animate-3' style='margin-top:0;'>🚀 Refactoring Roadmap</h3>", unsafe_allow_html=True)
    suggestions = audit.get("suggestions", [])
    priorities = ["🔴 HIGH PRIORITY", "🟡 MEDIUM PRIORITY", "🟢 LOW PRIORITY"]
    colors = ["#ff5252", "#ffb300", "#4CAF50"]
    gains = [8,4,2]
    
    cols = st.columns(3)
    for i in range(min(3, len(suggestions))):
        with cols[i]:
            priority_card(suggestions[i], priorities[i], gains[i], colors[i])

st.divider()

# -------------------------------------------------
# 🛠️ Inline Bullet Point Optimizer
# -------------------------------------------------
st.markdown("<h2 class='animate-3' style='margin-top:0;'>🛠️ Bullet Point Optimizer</h2>", unsafe_allow_html=True)
st.markdown("<p class='animate-3' style='color:#8F8F8F; font-size:15px; margin-bottom:30px;'>We identified bullet points in your resume that lack impact. Use AI to upgrade them instantly without fabricating information.</p>", unsafe_allow_html=True)

# 1. Helper function to route prompts with STRICT output rules
def rewrite_bullet(bullet, mode="rewrite"):
    prompts = {
        "rewrite": "Rewrite this resume bullet point professionally. Keep the original meaning. Do not invent any new metrics, achievements, or skills.",
        "stronger": "Rewrite this resume bullet point using stronger action verbs. Do not invent any new achievements, skills, or metrics.",
        "ats": "Rewrite this resume bullet point to be ATS-optimized. Naturally include relevant technical keywords based on the context. Do not add false information.",
        "another": "Generate an alternative professional version of this resume bullet point. Do not invent anything."
    }
    
    system_prompt = prompts.get(mode, prompts["rewrite"])
    
    strict_rules = """
    CRITICAL OUTPUT RULES:
    1. Output EXACTLY ONE single rewritten bullet point.
    2. DO NOT provide multiple options.
    3. DO NOT include any conversational filler (e.g., do NOT say "Here is a rewrite:").
    4. Return ONLY the raw text of the final rewritten sentence.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite", 
            contents=f"Instructions: {system_prompt}\n{strict_rules}\n\nOriginal Text: {bullet}"
        )
        
        # Failsafe for blocked content
        if not response.candidates or not response.candidates[0].content.parts:
            return "🚨 Error: Gemini returned an empty response."
            
        clean_text = response.text.strip()
        
        # Aggressively strip out Markdown formatting and conversational prefixes
        clean_text = clean_text.replace("**", "")
        if clean_text.startswith(("- ", "* ")):
            clean_text = clean_text[2:]
        if clean_text.startswith('"') and clean_text.endswith('"'):
            clean_text = clean_text[1:-1]
            
        return clean_text.strip()
        
    except Exception as e:
        return f"🚨 API Crash: {str(e)}"

# 2. Safely extract and sanitize the bullets from the audit data
raw_bullets = audit.get("weak_bullets", [])
if isinstance(raw_bullets, str): # Failsafe if AI returned a single string instead of a list
    raw_bullets = [raw_bullets]

# Filter out empty strings or weird whitespace that breaks the UI
weak_bullets = [b for b in raw_bullets if isinstance(b, str) and b.strip() and b.strip().lower() != "none"]

# 3. Render the UI
if not weak_bullets:
    # Success State: No weak bullets found
    st.markdown("""
    <div class="animate-3" style="background:rgba(76, 175, 80, 0.1); border-left:4px solid #4CAF50; padding:16px; border-radius:8px; color:#E0E0E0; font-size:16px;">
        🎉 <b>Excellent work!</b> The AI did not detect any weak or poorly phrased bullet points in your resume.
    </div>
    """, unsafe_allow_html=True)
else:
    # Action State: Draw the cards for the weak bullets
    for i, bullet in enumerate(weak_bullets):
        state_key = f"rewrite_{i}"
        
        # Original Bullet Card
        st.markdown(f"""
        <div class="animate-3" style="background:#171A21; border:1px solid #2D3342; border-left:4px solid #F4511E; border-radius:12px; padding:20px; margin-bottom:12px;">
            <div style="color:#F4511E; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Original Bullet</div>
            <div style="color:#E0E0E0; font-size:16px;">{bullet}</div>
        </div>
        """, unsafe_allow_html=True)

        # State 1: Before Rewrite
        if state_key not in st.session_state:
            btn_col, _ = st.columns([1, 3])
            with btn_col:
                if st.button("✨ Rewrite with AI", key=f"btn_rewrite_{i}", type="primary", width="stretch"):
                    with st.spinner("Optimizing bullet point..."):
                        st.session_state[state_key] = rewrite_bullet(bullet, "rewrite")
                        st.session_state[f"badge_{i}"] = "⭐⭐⭐⭐☆ Professional Level"
                        st.rerun()
                        
        # State 2: After Rewrite
        else:
            badge_text = st.session_state.get(f"badge_{i}", "⭐⭐⭐⭐☆ Professional Level")
            
            # Optimized Output Header
            st.markdown(f"""
            <div class="animate-3" style="background:rgba(76, 175, 80, 0.05); border:1px solid #2D3342; border-left:4px solid #4CAF50; border-radius:12px 12px 0 0; padding:15px 20px 10px 20px; border-bottom: none;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="color:#4CAF50; font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">Optimized Output</div>
                    <div style="background:#1E222B; border:1px solid #2D3342; padding:4px 10px; border-radius:999px; color:#A0AAB5; font-size:11px; font-weight:700;">{badge_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Native Streamlit code block
            st.code(st.session_state[state_key], language="markdown")
            
            # Sub-Actions
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔄 Another Version", key=f"v2_{i}", width="stretch"):
                    st.session_state[state_key] = rewrite_bullet(bullet, "another")
                    st.session_state[f"badge_{i}"] = "⭐⭐⭐⭐☆ Professional Level"
                    st.rerun()
            with c2:
                if st.button("⭐ Stronger", key=f"str_{i}", width="stretch"):
                    st.session_state[state_key] = rewrite_bullet(bullet, "stronger")
                    st.session_state[f"badge_{i}"] = "🔥 High Impact"
                    st.rerun()
            with c3:
                if st.button("🎯 ATS-Optimized", key=f"ats_{i}", width="stretch"):
                    st.session_state[state_key] = rewrite_bullet(bullet, "ats")
                    st.session_state[f"badge_{i}"] = "🟢 ATS Friendly"
                    st.rerun()
                    
        st.markdown("<br>", unsafe_allow_html=True)



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