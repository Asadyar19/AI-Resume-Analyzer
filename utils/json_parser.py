import json

def parse_gemini_json(text: str):
    """
    Parses JSON returned by Gemini.
    Removes Markdown code fences if Gemini wraps the JSON.
    Returns the parsed dictionary, or None if parsing fails.
    """
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)
    except Exception as e:
        print(f"JSON Parsing Error: {e}\nRaw Text: {text}")
        return None