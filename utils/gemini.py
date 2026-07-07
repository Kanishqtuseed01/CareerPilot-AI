import os
import json
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text, ats_score):

    prompt = f"""
You are an expert Career Coach.

The ATS engine has already calculated the score.

ATS Score:

{ats_score}

Resume:

{resume_text}

Do NOT calculate any score.

Return ONLY valid JSON.

Return exactly this format:

{{
    "feedback":"",
    "strengths":[],
    "weaknesses":[],
    "missing_keywords":[],
    "formatting_feedback":[],
    "action_items":[]
}}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            return text.strip()

        except Exception:

            if attempt == 2:
                raise

            time.sleep(5)