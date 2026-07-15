def ats_prompt(resume_text, job_description):

    return f"""
You are a senior Technical Recruiter and ATS (Applicant Tracking System) expert.

Analyze the resume against the provided job description.

Base your evaluation ONLY on the information provided.

Do NOT invent skills, experience, certifications, or projects.

Return your response in Markdown using exactly this structure:

# ATS Score
XX/100

# Matched Skills
- Skill 1
- Skill 2
- Skill 3

# Missing Skills
- Skill 1
- Skill 2
- Skill 3

# Resume Improvement Suggestions
1. Suggestion
2. Suggestion
3. Suggestion

Resume:
{resume_text}

Job Description:
{job_description}
"""