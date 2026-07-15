def extraction_prompt(resume_text, job_description):

    return f"""
You are an expert ATS parser.

Your ONLY task is to extract skills from the resume and job description.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do NOT wrap the JSON inside ```json.
3. Do NOT explain anything.
4. Do NOT include markdown.
5. Do NOT invent skills.
6. If a skill is not explicitly present, DO NOT include it.
7. For identical input, return identical output every time.
8. Remove duplicate skills.
9. Normalize ONLY these synonyms:

- JS → JavaScript
- AI → Artificial Intelligence
- ML → Machine Learning
- LLM → Large Language Models
- NLP → Natural Language Processing
- OOP → Object-Oriented Programming
- DSA → Data Structures and Algorithms
- VS Code → Visual Studio Code
- AWS → Amazon Web Services
- GCP → Google Cloud Platform

Return EXACTLY this JSON:

{{
    "resume_skills": [],
    "required_skills": [],
    "preferred_skills": []
}}

Resume:

{resume_text}

Job Description:

{job_description}
"""