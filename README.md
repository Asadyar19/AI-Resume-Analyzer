# 🚀 AI Resume Intelligence Platform

An AI-powered Resume Intelligence Platform built with **Python**, **Streamlit**, and **Google Gemini** that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS), improve resume quality, and compare resumes against real job descriptions using advanced AI analysis.

---

## ✨ Features

### 📄 AI Resume Auditor
- ATS Readiness Score
- Resume Quality Analysis
- Recruiter's First Impression
- Resume Statistics
- Keyword Density Analysis
- Missing Resume Sections Detection
- AI-Powered Bullet Point Optimizer
- Professional PDF Report Generation

### 🎯 Resume vs Job Matcher
- ATS Match Score
- Required & Preferred Skill Matching
- Missing Skills Detection
- Recruiter Compatibility Analysis
- Keyword Cloud Visualization
- Actionable Improvement Suggestions

---

## 🛠 Tech Stack

### Frontend
- Streamlit
- HTML
- CSS
- Plotly

### Backend
- Python

### AI
- Google Gemini API

### PDF Processing
- pdfplumber
- FPDF

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py
├── pages/
│   ├── resume_auditor.py
│   ├── resume_report.py
│   ├── jdmatcher.py
│   └── jdmatcher_report.py
│
├── utils/
│   ├── ats.py
│   ├── extractor.py
│   ├── gemini_client.py
│   ├── json_parser.py
│   ├── pdf_generator.py
│   ├── pdf_reader.py
│   ├── prompts.py
│   ├── resume_audit.py
│   └── sidebar.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Asadyar19/AI-Resume-Analyzer.git
```

Move into the project directory

```bash
cd AI-Resume-Analyzer
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
streamlit run app.py
```

---

## 🎯 Future Roadmap

Version 2 will include:

- AI Resume Tailoring
- AI Cover Letter Generator
- Resume Comparison
- Resume Score History
- DOCX Export
- User Authentication
- Cloud Database Integration

---

## 📸 Screenshots

> Add screenshots of the Home page, Resume Auditor, Job Matcher, and PDF Report here.

---

## 👨‍💻 Author

**Muhammad Asad Yar Khan**

BS Information Technology  
Bahria University Islamabad

GitHub: https://github.com/Asadyar19

---

## 📜 License

This project is licensed under the MIT License.