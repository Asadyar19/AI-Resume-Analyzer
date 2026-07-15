import json


def parse_gemini_json(text: str):
    """
    Parses JSON returned by Gemini.
    Removes Markdown code fences if Gemini wraps the JSON.
    """

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)