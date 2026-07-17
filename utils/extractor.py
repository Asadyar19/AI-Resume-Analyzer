from google.genai import types
from utils.gemini_client import client
from utils.prompts import extraction_prompt
from utils.json_parser import parse_gemini_json # Adjust import path as needed

def extract_skills(resume_text, job_description):
    prompt = extraction_prompt(
        resume_text,
        job_description
    )

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            top_p=0,
        )
    )

    # Use your centralized parser
    data = parse_gemini_json(response.text)
    
    # Failsafe if the parser returned None
    if not data:
        data = {}

    return {
        "resume_skills": sorted(
            list(set(data.get("resume_skills", [])))
        ),
        "required_skills": sorted(
            list(set(data.get("required_skills", [])))
        ),
        "preferred_skills": sorted(
            list(set(data.get("preferred_skills", [])))
        )
    }