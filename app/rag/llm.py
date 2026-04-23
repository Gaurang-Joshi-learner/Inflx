from google import genai
from dotenv import dotenv_values
from pathlib import Path

# load API key
BASE_DIR = Path(__file__).resolve().parents[2]
env = dotenv_values(BASE_DIR / ".env")

client = genai.Client(api_key=env.get("GOOGLE_AI_API_KEY"))


def generate_answer(query: str, context: str, history: str):
    prompt = f"""
You are an AI assistant for AutoStream.

Conversation History:
{history}

Context:
{context}

User Question:
{query}

Rules:
- Use context
- Use conversation history if relevant
- Be helpful and natural
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
            config={"temperature": 0.4}
        )

        answer = response.text.strip()

        # 🔥 fallback handling
        if "not sure" in answer.lower():
            return "Let me connect you with our team for better assistance."

        return answer

    except Exception as e:
        print("LLM Error:", e)
        return "Something went wrong. Please try again."