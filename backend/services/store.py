import time
from typing import Dict

class SessionStore:
    def __init__(self):
        self.store: Dict[str, dict] = {}

    def create(self, session_id: str, meta: dict, questions: list):
        self.store[session_id] = {
            "meta": meta,
            "questions": questions,
            "answers": [],
            "created_at": time.time(),
            "status": "ongoing"
        }

    def get(self, session_id: str):
        return self.store.get(session_id)

    def save_answer(self, session_id: str, answer_obj: dict):
        session = self.store.get(session_id)
        if not session:
            raise KeyError("Session not found")
        session["answers"].append(answer_obj)

    def finalize(self, session_id: str, report: dict):
        session = self.store.get(session_id)
        if not session:
            raise KeyError("Session not found")
        session["final_report"] = report
        session["status"] = "completed"
