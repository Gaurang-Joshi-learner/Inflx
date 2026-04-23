from dotenv import dotenv_values
from pathlib import Path
from google import genai
import json
import re

# -------- LOAD ENV --------
BASE_DIR = Path(__file__).resolve().parents[2]
env = dotenv_values(BASE_DIR / ".env")

client = genai.Client(api_key=env.get("GOOGLE_AI_API_KEY"))


# -------- HELPER --------
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"intent": "inquiry"}


# -------- MAIN FUNCTION --------
def classify_intent(message: str) -> str:
    msg = message.lower().strip()

    # -------- HARD RULES --------

    # Greeting
    if any(x in msg for x in ["hi", "hello", "hey"]):
        return "greeting"

    # Pricing MUST stay inquiry
    if any(x in msg for x in [
        "price",
        "pricing",
        "cost",
        "how much"
    ]):
        return "inquiry"

    # -------- STRONG HIGH INTENT ONLY --------
    if any(x in msg for x in [
        "i want pro",
        "i want basic",
        "subscribe",
        "buy",
        "sign up",
        "get started",
        "start now",
        "i will take"
    ]):
        return "high_intent"

    # -------- GEMINI FALLBACK --------
    try:
        prompt = f"""
Classify into:
- greeting
- inquiry
- high_intent

Return ONLY JSON:
{{ "intent": "..." }}

Message: {message}
"""

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
            config={"temperature": 0}
        )

        text = response.text.strip()
        print("Gemini Raw:", text)

        data = extract_json(text)

        intent = data.get("intent", "inquiry")

        if intent not in ["greeting", "inquiry", "high_intent"]:
            return "inquiry"

        return intent

    except Exception as e:
        print("Gemini Error:", e)
        return "inquiry"