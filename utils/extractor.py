import json

from google.genai import types

from utils.gemini_client import client
from utils.prompts import extraction_prompt


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

    text = response.text.strip()

    # Remove markdown fences if Gemini accidentally adds them
    if text.startswith("```"):

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    data = json.loads(text)

    return {
        "resume_skills": sorted(
            list(
                set(data.get("resume_skills", []))
            )
        ),
        "required_skills": sorted(
            list(
                set(data.get("required_skills", []))
            )
        ),
        "preferred_skills": sorted(
            list(
                set(data.get("preferred_skills", []))
            )
        )
    }