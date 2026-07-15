SKILL_WEIGHTS = {
    # Programming Languages
    "Python": 5,
    "C++": 5,
    "C#": 4,
    "JavaScript": 4,
    "SQL": 4,
    "HTML": 2,
    "CSS": 2,

    # AI / ML
    "Machine Learning": 5,
    "Artificial Intelligence": 5,
    "Large Language Models": 5,
    "Natural Language Processing": 5,
    "TensorFlow": 5,
    "PyTorch": 5,
    "Scikit-learn": 5,
    "Prompt Engineering": 4,
    "Generative AI": 4,
    "Retrieval-Augmented Generation": 4,
    "LangChain": 4,
    "LlamaIndex": 4,

    # Data Science
    "NumPy": 4,
    "Pandas": 4,

    # Cloud
    "Amazon Web Services": 3,
    "Google Cloud Platform": 3,

    # DevOps
    "Docker": 3,
    "Linux": 3,
    "REST APIs": 3,

    # Databases
    "SQL Server": 3,
    "Oracle 11g": 3,

    # Security
    "SSL/TLS": 2,
    "OpenSSL": 2,

    # Developer Tools
    "Git": 2,
    "GitHub": 2,
    "Visual Studio": 1,
    "VS Code": 1,
    "PyQt": 1,
    "Ollama": 2,
    "Gemini API": 2,
    "Vapi AI": 2,
    "n8n": 2,

    # CS Fundamentals
    "Data Structures and Algorithms": 4,
    "Object-Oriented Programming": 4,
}


def calculate_ats_score(resume_skills, job_skills):

    resume = set(resume_skills)

    required = set(job_skills.get("required", []))
    preferred = set(job_skills.get("preferred", []))

    matched_required = resume & required
    matched_preferred = resume & preferred

    missing_required = required - resume
    missing_preferred = preferred - resume

    # -----------------------------
    # Weighted Score
    # -----------------------------
    required_total = 0
    required_match = 0

    for skill in required:
        weight = SKILL_WEIGHTS.get(skill, 3)
        required_total += weight

        if skill in resume:
            required_match += weight

    preferred_total = 0
    preferred_match = 0

    for skill in preferred:
        weight = SKILL_WEIGHTS.get(skill, 2)
        preferred_total += weight

        if skill in resume:
            preferred_match += weight

    required_score = (
        required_match / required_total
        if required_total
        else 1
    )

    preferred_score = (
        preferred_match / preferred_total
        if preferred_total
        else 1
    )

    # Required contributes 80%
    # Preferred contributes 20%
    score = round(
        (required_score * 80) +
        (preferred_score * 20)
    )

    matched = sorted(
        matched_required | matched_preferred
    )

    missing = sorted(
        missing_required | missing_preferred
    )

    return score, matched, missing