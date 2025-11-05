import os
import json
import re
from dotenv import load_dotenv
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "..", ".env")

# Default models
DEFAULT_MODELS = {
    "gemini": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "groq": os.getenv("GROQ_MODEL", "mixtral-8x7b")
}


def safe_parse_json(text: str):
    """Safely parse text into JSON or return fallback structure."""
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"(\{.*\}|\[.*\])", text, re.S)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        return {"raw": text}


def handle_api_error(provider: str, error: Exception):
    """Detect API key, quota, or model issues and return friendly messages."""
    err = str(error).lower()

    key_related = [
        "api key", "invalid", "expired", "unauthorized", "authentication",
        "invalidapikey", "invalid_request_error", "access denied", "401", "403"
    ]
    quota_related = ["quota", "billing", "limit", "trial", "insufficient_quota"]
    model_related = ["not found", "unsupported", "invalid model"]

    if any(k in err for k in key_related):
        return f"❌ Invalid or expired API key for {provider.title()}.", True
    elif any(k in err for k in quota_related):
        return f"⚠️ API quota or trial limit reached for {provider.title()}.", False
    elif any(k in err for k in model_related):
        return f"⚠️ Model not found or unsupported for {provider.title()}.", False
    else:
        return f"❗ Unexpected error with {provider.title()} API: {error}", False


def _generate_response(
    prompt: str,
    max_new_tokens: int = 600,
    temperature: float = 0.2,
    provider: str = "gemini",
    api_key: str = None,
    model: str = None
):
    """
    Unified dynamic LLM API router with fallback key logic:
    1️⃣ Try user-provided key (if any)
    2️⃣ On key-related error, retry with .env key
    3️⃣ Only fail if both are invalid or missing
    """
    provider = provider.lower().strip()
    model = model or DEFAULT_MODELS.get(provider)

    user_key = api_key.strip() if api_key else None
    env_key = os.getenv(f"{provider.upper()}_API_KEY")

    if not (user_key or env_key):
        return json.dumps({
            "error": f"❌ No API key provided for {provider.title()}. Please add one manually or in .env"
        })

    def call_provider(final_key):
        if provider == "gemini":
            if not genai:
                raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
            genai.configure(api_key=final_key)
            llm = genai.GenerativeModel(model)
            resp = llm.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_new_tokens},
            )
            return resp.text.strip() if resp and getattr(resp, "text", None) else ""

        elif provider == "groq":
            if not Groq:
                raise ImportError("groq package not installed. Run: pip install groq")
            client = Groq(api_key=final_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_new_tokens,
            )
            return resp.choices[0].message.content.strip()

        elif provider == "openai":
            if not OpenAI:
                raise ImportError("openai package not installed. Run: pip install openai")
            client = OpenAI(api_key=final_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_new_tokens,
            )
            return resp.choices[0].message.content.strip()

        else:
            raise ValueError(f"❌ Unsupported provider: {provider}")

    # Try user key first
    if user_key:
        try:
            return call_provider(user_key)
        except Exception as e:
            msg, key_error = handle_api_error(provider, e)
            # Retry with env key only for key-related errors
            if key_error and env_key:
                try:
                    return call_provider(env_key)
                except Exception as e2:
                    msg2, _ = handle_api_error(provider, e2)
                    return json.dumps({"error": msg2})
            return json.dumps({"error": msg})

    # If no user key, try env key directly
    try:
        return call_provider(env_key)
    except Exception as e:
        msg, _ = handle_api_error(provider, e)
        return json.dumps({"error": msg})


# ------------------ GENERATE QUESTIONS ------------------

def generate_questions(role, domain, experience, mode, num=4, api_key=None, provider="gemini"):
    """Generate structured interview questions dynamically."""
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

    text = _generate_response(prompt, max_new_tokens=600, provider=provider, api_key=api_key)
    parsed = safe_parse_json(text)

    # Handle provider or API errors
    if isinstance(parsed, dict) and "error" in parsed:
        return parsed

    # Fallback if model output is invalid
    if isinstance(parsed, dict) and "raw" in parsed:
        return [
            {
                "id": i,
                "question": f"Tell me about a challenge you faced as a {role}. (fallback Q{i})",
                "type": mode,
                "difficulty": "medium",
                "hint": "",
            }
            for i in range(1, num + 1)
        ]
    return parsed


# ------------------ EVALUATE ANSWER ------------------

def evaluate_answer(question_obj, answer_text, mode, experience, api_key=None, provider="gemini"):
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

    text = _generate_response(prompt, max_new_tokens=700, provider=provider, api_key=api_key)
    parsed = safe_parse_json(text)

    if isinstance(parsed, dict) and "error" in parsed:
        return parsed

    if isinstance(parsed, dict) and "raw" in parsed:
        return {
            "question_id": qid,
            "scores": {"technical": 5, "communication": 5, "confidence": 5},
            "feedback": parsed["raw"],
            "examples_or_corrections": "",
            "resources": [],
        }
    return parsed
