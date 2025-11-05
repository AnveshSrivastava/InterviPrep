from pydantic import BaseModel
from typing import Optional, List, Dict

class StartRequest(BaseModel):
    role: str
    domain: str
    experience: str
    mode: str
    model_provider: Optional[str] = None
    api_key: Optional[str] = None
    # provider field optional — not needed if you use model_provider
class Question(BaseModel):
    id: int
    question: str
    type: Optional[str] = None
    difficulty: Optional[str] = None
    hint: Optional[str] = None

class StartResponse(BaseModel):
    session_id: str
    questions: List[Question]

class AnswerRequest(BaseModel):
    question_id: int
    answer: str

class EvalResponse(BaseModel):
    question_id: int
    scores: Dict[str,int]
    feedback: str
    examples_or_corrections: Optional[str] = None
    resources: Optional[List[str]] = None
