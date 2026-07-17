from fpdf import FPDF

def sanitize(text):
    if not isinstance(text, str): return ""
    return text.encode('ascii', 'ignore').decode('ascii').strip()

def get_grade(score):
    try:
        s = float(score)
        if s >= 90: return "A"
        if s >= 80: return "B"
        if s >= 70: return "C"
        return "D"
    except: return "N/A"

class PremiumPDF(FPDF):
    def header(self):
        # Deep Navy Header
        self.set_fill_color(33, 43, 54)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 20)
        self.set_xy(0, 8)
        self.cell(210, 10, "Professional Resume Analysis Report", align="C")
        
        # Accent Line
        self.set_fill_color(76, 175, 80)
        self.rect(0, 30, 210, 2, 'F')

    def footer(self):
        self.set_y(-18)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, "Generated securely via AI Engine", align="C")
        self.set_y(-14)
        self.set_font("helvetica", "B", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "System Engineered by M. Asad Yar Khan", align="C")

def generate_audit_pdf(audit_data):
    if not isinstance(audit_data, dict): audit_data = {}
    
    pdf = PremiumPDF()
    pdf.add_page()
    pdf.set_margins(10, 35, 10)
    pdf.set_auto_page_break(auto=False) # Disable auto-break to force fit
    
    # 1. CANDIDATE NAME
    pdf.set_y(35)
    pdf.set_x(10) 
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(190, 10, f"Candidate: {sanitize(audit_data.get('candidate_name', 'Candidate'))}", ln=1)
    
    # 2. SUMMARY STRIP
    pdf.set_x(10)
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 12, 'F')
    pdf.set_font("helvetica", "B", 9)
    pdf.set_text_color(80, 80, 80)
    y_pos = pdf.get_y() + 4
    pdf.set_xy(10, y_pos)
    pdf.cell(63, 6, f"OVERALL GRADE: {audit_data.get('grade', 'N/A')}", align="C")
    pdf.cell(63, 6, f"ATS READY: {audit_data.get('ats_ready', 'No')}", align="C")
    pdf.cell(64, 6, f"RECRUITER READY: {audit_data.get('recruiter_ready', 'No')}", align="C")
    pdf.ln(12)

    # 3. VERDICT BOX
    pdf.set_x(10)
    pdf.set_fill_color(232, 245, 233)
    pdf.set_draw_color(76, 175, 80)
    pdf.rect(10, pdf.get_y(), 190, 22, 'FD')
    pdf.set_text_color(46, 125, 50)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_xy(12, pdf.get_y() + 2)
    pdf.cell(186, 5, "Recruiter Verdict", ln=1)
    pdf.set_font("helvetica", "", 9)
    pdf.set_x(12)
    pdf.multi_cell(186, 4, sanitize(audit_data.get("verdict_text", "")), align="L")
    pdf.ln(8)

    # 4. PERFORMANCE BREAKDOWN
    pdf.set_x(10)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(190, 8, "Performance Breakdown", ln=1)
    
    # Table Header
    pdf.set_x(10)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(100, 8, "Metric", 1, 0, 'C', True)
    pdf.cell(45, 8, "Score", 1, 0, 'C', True)
    pdf.cell(45, 8, "Grade", 1, 1, 'C', True)
    
    # Table Rows
    pdf.set_font("helvetica", "", 10)
    for label, info in audit_data.get("metrics", {}).items():
        score = info.get("score", info) if isinstance(info, dict) else info
        pdf.set_x(10)
        pdf.cell(100, 8, label.replace("_", " ").title(), 1)
        pdf.cell(45, 8, str(score), 1, 0, 'C')
        pdf.cell(45, 8, get_grade(score), 1, 1, 'C')
    pdf.ln(6)

    # 5. SECTIONS
    def add_section(title, items, r, g, b):
        if not items: return
        pdf.set_x(10)
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(190, 8, f"  {title}", 0, 1, 'L', True)
        pdf.set_text_color(60, 60, 60)
        pdf.set_font("helvetica", "", 9)
        pdf.ln(2)
        for item in items:
            pdf.set_x(12)
            pdf.multi_cell(186, 6, sanitize(item), 0, 'L')
        pdf.ln(3)

    add_section("Key Strengths", audit_data.get("strengths", []), 33, 150, 243)
    add_section("Critical Weaknesses", audit_data.get("weaknesses", []), 239, 83, 80)
    add_section("Recommended Next Steps", audit_data.get("suggestions", []), 255, 152, 0)
    
    return bytes(pdf.output())