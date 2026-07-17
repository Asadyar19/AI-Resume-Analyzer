import streamlit as st

def render_custom_sidebar(active_page="home"):
    """
    Renders a premium, high-density HTML sidebar inspired by Cursor and OpenAI.
    Includes an enhanced faint neon ambient glow on the active page link.
    """
    
    # 1. Configure Navigation Layout Items (Using OS-Independent Icons)
    menu_items = [
        {"id": "home", "label": "⌂ &nbsp; Home", "path": "/"},
        {"id": "job_matcher", "label": "◎ &nbsp; Job Matcher", "path": "/jdmatcher"},
        {"id": "resume_auditor", "label": "◫ &nbsp; Resume Auditor", "path": "/resume_auditor"}
    ]
    
    # 2. Build the Menu Components
    menu_html = ""
    for item in menu_items:
        is_active = "active" if item["id"].lower() == active_page.lower() else ""
        menu_html += f'<a href="{item["path"]}" target="_self" class="nav-item {is_active}">{item["label"]}</a>'

    # 3. UI Markup Template (Zero Tabs/Indentations to protect against Markdown leaks)
    sidebar_html = f"""
<input type="checkbox" id="sidebar-panel-toggle" class="sidebar-state-checkbox">
<label for="sidebar-panel-toggle" class="floating-console-trigger">≡</label>
<div class="custom-sidebar">
<div class="sidebar-top-wrapper">
<div class="sidebar-brand-container">
<div class="brand-title">🧠 Resume Intelligence</div>
<div class="brand-subtitle">Professional AI Suite</div>
</div>
<label for="sidebar-panel-toggle" class="inner-console-trigger">≡</label>
</div>
<div class="sidebar-divider"></div>
<div class="sidebar-middle-wrapper">
<div class="sidebar-section-label">Navigation</div>
{menu_html}
</div>
<div class="sidebar-bottom-wrapper">
<div class="sidebar-divider"></div>
<div class="sidebar-section-label">AI Status</div>
<div class="status-item"><span class="status-dot active-dot">●</span> Gemini Connected</div>
<div class="status-item"><span class="status-dot active-dot">●</span> ATS Engine Ready</div>
<div class="status-item"><span class="status-dot active-dot">●</span> Version 1.0</div>
<div class="sidebar-divider"></div>
<div class="sidebar-copyright">© Asad Yar Khan</div>
</div>
</div>
<style>
section[data-testid="stSidebar"], 
button[data-testid="stSidebarCollapseAction"],
div[data-testid="collapsedControl"] {{
    display: none !important;
}}
.sidebar-state-checkbox {{
    display: none !important;
}}
div[data-testid="stAppViewContainer"] {{
    margin-left: 280px !important;
    width: calc(100% - 280px) !important;
    padding-left: 0px !important;
    transition: margin-left 0.25s cubic-bezier(0.4, 0, 0.2, 1), width 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}
.custom-sidebar {{
    position: fixed;
    top: 0;
    left: 0;
    width: 260px;
    height: 100vh;
    background-color: #0A0D14;
    border-right: 1px solid #1C202C;
    padding: 24px 16px;
    box-sizing: border-box;
    z-index: 999999;
    font-family: 'Segoe UI', system-ui, sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}}
.sidebar-top-wrapper {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
}}
.sidebar-middle-wrapper {{
    flex-grow: 1;
    margin-top: 16px;
}}
.sidebar-brand-container {{
    padding-left: 4px;
}}
.brand-title {{
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.3px;
    margin-bottom: 2px;
}}
.brand-subtitle {{
    font-size: 12px;
    font-weight: 500;
    color: #6C7284;
}}
.sidebar-section-label {{
    font-size: 10px;
    font-weight: 700;
    color: #4A5060;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
    padding-left: 8px;
}}
.sidebar-divider {{
    height: 1px;
    background-color: #1C202C;
    margin: 20px 0;
    width: 100%;
}}
.nav-item {{
    display: flex !important;
    align-items: center !important;
    color: #A0A5B5 !important;
    text-decoration: none !important;
    padding: 12px 16px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-left: 4px solid transparent !important;
}}
.nav-item:hover {{
    color: #4CAF50 !important;
    background-color: rgba(76, 175, 80, 0.04) !important;
    transform: translateX(2px) scale(1.01);
}}
/* Premium Active Navigation State with Faint Glow Container */
.nav-item.active {{
    color: #FFFFFF !important;
    background: linear-gradient(90deg, rgba(76, 175, 80, 0.14), rgba(76, 175, 80, 0.02)) !important;
    border-left: 4px solid #4CAF50 !important;
    border-radius: 4px 8px 8px 4px !important;
    font-weight: 700 !important;
    /* Faint ambient drop glow + clean inner definition shadow */
    box-shadow: 0 4px 24px rgba(76, 175, 80, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    text-shadow: 0 0 12px rgba(255, 255, 255, 0.2);
}}
.status-item {{
    display: flex;
    align-items: center;
    font-size: 13px;
    color: #8A90A2;
    padding: 6px 8px;
    font-weight: 500;
}}
.status-dot {{
    font-size: 9px;
    margin-right: 10px;
}}
.active-dot {{
    color: #4CAF50;
    text-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
}}
.system-dot {{
    color: #4A5060;
    margin-left: 2px;
}}
.sidebar-copyright {{
    font-size: 12px;
    font-weight: 600;
    color: #525866;
    padding-left: 8px;
    margin-top: 4px;
}}
.inner-console-trigger, .floating-console-trigger {{
    font-family: sans-serif !important;
    font-size: 24px !important;
    font-weight: bold !important;
    color: #4CAF50;
    cursor: pointer;
    transition: all 0.2s ease;
}}
.inner-console-trigger {{
    padding: 2px 8px;
    border-radius: 6px;
    margin-top: -6px;
}}
.inner-console-trigger:hover {{
    background-color: rgba(76, 175, 80, 0.08);
    color: #6DFF7B;
}}
.floating-console-trigger {{
    display: none;
    position: fixed;
    top: 20px;
    left: 20px;
    background-color: #111520;
    border: 1px solid #222836;
    padding: 6px 14px 10px 14px;
    border-radius: 8px;
    z-index: 999998;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    line-height: 1 !important;
}}
.floating-console-trigger:hover {{
    color: #6DFF7B;
    border-color: #4CAF50;
    transform: translateY(-1px);
}}
body:has(#sidebar-panel-toggle:checked) div[data-testid="stAppViewContainer"] {{
    margin-left: 0px !important;
    width: 100% !important;
}}
body:has(#sidebar-panel-toggle:checked) .custom-sidebar {{
    transform: translateX(-260px);
}}
body:has(#sidebar-panel-toggle:checked) .floating-console-trigger {{
    display: block !important;
}}
@media (max-width: 992px) {{
    div[data-testid="stAppViewContainer"] {{
        margin-left: 0px !important;
        width: 100% !important;
    }}
    .custom-sidebar {{
        transform: translateX(-260px);
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.5);
    }}
    .floating-console-trigger {{
        display: block !important;
    }}
    body:has(#sidebar-panel-toggle:checked) .custom-sidebar {{
        transform: translateX(0px);
    }}
    body:has(#sidebar-panel-toggle:checked) .floating-console-trigger {{
        display: none !important;
    }}
}}
</style>
"""
    st.markdown(sidebar_html, unsafe_allow_html=True)