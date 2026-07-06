import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume carefully.

Return ONLY valid JSON.

Do not explain anything.
Do not use markdown.
Do not use ```json.

Return exactly this format:

{{
    "overall_score": 0,
    "section_scores": {{
        "contact_information": 0,
        "professional_summary": 0,
        "education": 0,
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "ats_keywords": 0,
        "formatting": 0
    }},
    "feedback": "",
    "strengths": [],
    "weaknesses": [],
    "missing_keywords": [],
    "ats_keywords": [],
    "formatting_feedback": [],
    "action_items": []
}}

Resume:

{resume_text}
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "temperature": 0
                }
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            return text

        except Exception as e:

            if attempt == 2:
                raise e

            time.sleep(5)