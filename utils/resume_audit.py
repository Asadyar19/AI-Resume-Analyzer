from utils.gemini_client import client
from utils.json_parser import parse_gemini_json

def audit_resume(resume_text):
    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume evaluator.

SCORING INSTRUCTIONS:
Evaluate the provided resume objectively, fairly, and accurately based on standard industry practices. 
Do NOT artificially deflate the overall scores. If the formatting and content are strong, score them high.
Do NOT compare it to any job description.
Return ONLY valid JSON.
Do NOT wrap the response in markdown.

CRITICAL EXTRACTION RULE - WEAK BULLETS:
Even in a high-scoring, excellent resume, there is always room for optimization. 
Independent of your overall high scores, you MUST extract between 2 and 4 of the LEAST impactful bullet points directly from the resume text. 
Look for bullets that:
1. Lack quantified metrics (numbers, percentages, timeframes, or financial impact).
2. Use passive language or weak starter verbs (e.g., "Worked on", "Helped with", "Responsible for", "Tasked with").
3. Describe a basic duty rather than a specific accomplishment or result.

Return these EXACT sentences word-for-word in the JSON under the key "weak_bullets" as a list of strings. DO NOT return an empty list.

Return this exact structure:
{{
    "candidate_name": "Full Name Found in Resume",
    "grade": "A",
    "ats_ready": "Yes",
    "recruiter_ready": "Good",
    "verdict_text": "A brief summary verdict.",
    "ats_score": 0,
    "sections": {{
        "contact_information": true,
        "education": true,
        "experience": true,
        "projects": true,
        "skills": true,
        "certifications": false
    }},
    "scores": {{
        "formatting": 0,
        "readability": 0,
        "keyword_density": 0,
        "bullet_points": 0,
        "action_verbs": 0,
        "quantified_achievements": 0
    }},
    "strengths": [
        "",
        "",
        ""
    ],
    "weaknesses": [
        "",
        "",
        ""
    ],
    "suggestions": [
        "",
        "",
        ""
    ],
    "weak_bullets": [
        "",
        ""
    ]
}}

Scoring Guidelines:
ATS Score: 0-100
Formatting: 0-100
Readability: 0-100
Keyword Density: 0-100
Bullet Points: 0-100
Action Verbs: 0-100
Quantified Achievements: 0-100

Resume:
{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    # Use your centralized parser
    parsed_data = parse_gemini_json(response.text)

    # Failsafe if the parser returned None (catastrophic AI failure)
    if not parsed_data:
        parsed_data = {
            "candidate_name": "Candidate",
            "grade": "N/A",
            "ats_ready": "No",
            "recruiter_ready": "Needs Work",
            "verdict_text": "Analysis pending.",
            "ats_score": 0, 
            "sections": {}, 
            "scores": {
                "formatting": 0, "readability": 0, "keyword_density": 0,
                "bullet_points": 0, "action_verbs": 0, "quantified_achievements": 0
            }, 
            "strengths": [], "weaknesses": [], "suggestions": [], "weak_bullets": []
        }

    # Ensure weak_bullets always exists to prevent UI crashes
    if "weak_bullets" not in parsed_data:
        parsed_data["weak_bullets"] = []

    # Ensure candidate_name always exists
    if "candidate_name" not in parsed_data:
        parsed_data["candidate_name"] = "Candidate"
        
    # Ensure grade, ats_ready, recruiter_ready, and verdict_text exist
    if "grade" not in parsed_data:
        parsed_data["grade"] = "N/A"
    if "ats_ready" not in parsed_data:
        parsed_data["ats_ready"] = "No"
    if "recruiter_ready" not in parsed_data:
        parsed_data["recruiter_ready"] = "Needs Work"
    if "verdict_text" not in parsed_data:
        parsed_data["verdict_text"] = "Review pending."

    # Map the existing 'scores' data to 'metrics' so the PDF generator works
    parsed_data["metrics"] = parsed_data.get("scores", {})

    return parsed_data