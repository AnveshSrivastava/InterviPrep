import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")

if not GEMINI_API_KEY:
    raise ValueError("❌ Missing GEMINI_API_KEY in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def safe_parse_json(text: str):
    """Tries to safely parse text into JSON; falls back if invalid."""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"(\{.*\}|\[.*\])", text, re.S)
        if m:
            blob = m.group(1)
            try:
                return json.loads(blob)
            except Exception:
                pass
        return {"raw": text}

def _generate_response(prompt: str, max_new_tokens: int = 600, temperature: float = 0.2):
    """Call Gemini API."""
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_new_tokens
        }
    )

    return response.text.strip() if response and response.text else ""

def generate_questions(role: str, domain: str, experience: str, mode: str, num: int = 4):
    """Generate structured interview questions."""
    role = role or "Software Engineer"
    domain_clause = f"in domain {domain}" if domain else ""

    prompt = f"""
You are an experienced interviewer. Output valid JSON only.

Generate {num} interview questions for a {mode} interview for a candidate applying to role "{role}" {domain_clause} with experience level "{experience}".

Return a JSON array like:
[
  {{ "id": 1, "question": "text", "type": "technical|behavioral|hr", "difficulty":"easy|medium|hard", "hint":"one-line hint" }},
  ...
]
"""
    text = _generate_response(prompt, max_new_tokens=600)
    parsed = safe_parse_json(text)

    if isinstance(parsed, dict) and "raw" in parsed:
        return [
            {
                "id": i,
                "question": f"Tell me about a challenge you faced in {role} role. (fallback Q{i})",
                "type": mode,
                "difficulty": "medium",
                "hint": "",
            }
            for i in range(1, num + 1)
        ]
    return parsed

def evaluate_answer(question_obj: dict, answer_text: str, mode: str, experience: str):
    """Evaluate a candidate's answer with structured scoring + feedback."""
    qid = question_obj.get("id", 0)
    question = question_obj.get("question", "")

    prompt = f"""
You are an expert interviewer & coach. Evaluate the candidate's answer.

Question: "{question}"
Candidate Answer: "{answer_text}"
Mode: {mode}
Experience: {experience}

Score on 3 scales (1-10):
- technical (or content accuracy)
- communication
- confidence & structure

Also provide:
- 3-line actionable feedback
- an improved example (if behavioral show STAR example, if technical show concise correction or recommended steps)
- 1-2 short resource links (just URLs or titles)

Return JSON only like:
{{
 "question_id": {qid},
 "scores": {{"technical": 0, "communication": 0, "confidence": 0}},
 "feedback": "short actionable feedback",
 "examples_or_corrections": "improved answer or short corrected steps",
 "resources": ["https://..."]
}}
"""
    text = _generate_response(prompt, max_new_tokens=700)
    parsed = safe_parse_json(text)

    if isinstance(parsed, dict) and "raw" in parsed:
        return {
            "question_id": qid,
            "scores": {"technical": 5, "communication": 5, "confidence": 5},
            "feedback": parsed["raw"],
            "examples_or_corrections": "",
            "resources": [],
        }
    return parsed
