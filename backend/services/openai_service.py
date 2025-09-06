import os
import json
import re
from dotenv import load_dotenv
import openai

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY not found. Please set it in backend/.env or environment.")

openai.api_key = OPENAI_KEY

def safe_parse_json(text: str):
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

def generate_questions(role: str, domain: str, experience: str, mode: str, num: int = 4):
    role = role or "Software Engineer"
    domain = domain or ""
    prompt = f"""
You are an experienced interviewer. Output valid JSON only.

Generate {num} interview questions for a {mode} interview for a candidate applying to role "{role}" {f'in domain {domain}' if domain else ''} with experience level "{experience}".

Return a JSON array like:
[
  {{ "id": 1, "question": "text", "type": "technical|behavioral|hr", "difficulty":"easy|medium|hard", "hint":"one-line hint" }},
  ...
]
"""
    resp = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=[{"role":"system","content":"You are an interviewer and career coach."},
                  {"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens=600
    )
    text = resp['choices'][0]['message']['content']
    parsed = safe_parse_json(text)
    if isinstance(parsed, dict) and "raw" in parsed:
        fallback = []
        for i in range(1, num+1):
            fallback.append({
                "id": i,
                "question": f"Tell me about a challenge you faced in {role} role. (fallback Q{i})",
                "type": mode,
                "difficulty": "medium",
                "hint": ""
            })
        return fallback
    return parsed

def evaluate_answer(question_obj: dict, answer_text: str, mode: str, experience: str):
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
    resp = openai.ChatCompletion.create(
        model=DEFAULT_MODEL,
        messages=[{"role":"system","content":"You are an expert interviewer and coach."},
                  {"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens=700
    )
    text = resp['choices'][0]['message']['content']
    parsed = safe_parse_json(text)
    if isinstance(parsed, dict) and "raw" in parsed:
        return {
            "question_id": qid,
            "scores": {"technical": 5, "communication": 5, "confidence": 5},
            "feedback": parsed["raw"],
            "examples_or_corrections": "",
            "resources": []
        }
    return parsed
