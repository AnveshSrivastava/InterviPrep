🤖 InterviewPrepBot

AI-powered mock interview platform. Generate interview questions, submit answers, get real-time AI evaluation, and view a final report with scores and feedback. Built with FastAPI backend + Streamlit frontend.

Project Structure
interview-bot/
├── backend/
│   ├── main.py
│   ├── routes/
│   │   └── interview.py
│   ├── services/
│   │   ├── openai_service.py
│   │   └── store.py
│   └── schemas.py
├── frontend/
│   └── app.py
├── .env.example
├── requirements.txt
└── README.md

Features

Generate technical and behavioral questions based on role, domain, and experience.

Submit answers and get AI-generated evaluation:

Scores (Technical, Communication, Confidence)

Feedback & improved example answers

Recommended resources

Final report with aggregated scores.

Streamlit UI for interactive session.

Fully hackathon-ready: works out-of-the-box with OpenAI API key.

Setup Instructions
1. Clone the repository
git clone https://github.com/yourusername/InterviewPrepBot.git
cd InterviewPrepBot

2. Create a Python virtual environment
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

4. Setup OpenAI API Key

Copy .env.example → backend/.env

Open backend/.env and replace:

OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY
DEFAULT_MODEL=gpt-3.5-turbo


Get your key from OpenAI API keys

Alternative (system environment variable):

Windows PowerShell:

$env:OPENAI_API_KEY="sk-..."


macOS/Linux:

export OPENAI_API_KEY="sk-..."

5. Run Backend (FastAPI)
cd backend
uvicorn main:app --reload --port 8000


Open Swagger docs
 to inspect API endpoints.

6. Run Frontend (Streamlit)
cd frontend
streamlit run app.py


Streamlit will open browser at http://localhost:8501

7. Using the App

Fill your name, role, domain, experience, and mode (technical/behavioral).

Click Start Mock Interview → questions are generated via AI.

Answer each question → click Submit to get AI evaluation.

Skip or Retry questions if needed.

Click Finish & Get Report → aggregated score and feedback.

8. Important Notes

Do not commit backend/.env or venv/ to GitHub.

Ensure CORS allows Streamlit: http://localhost:8501.

Slow OpenAI responses? Reduce question count or cache sample questions.

Frontend/Backend ports can be changed if in use.

9. Optional Enhancements

PDF export after finalize (pdfkit + Jinja2 template)

Voice input with Whisper for answer transcription

Store sessions in SQLite for persistence

Visual improvements in Streamlit UI

10. Troubleshooting
Error	Fix
OPENAI_API_KEY not found	Ensure backend/.env exists & API key is valid. Restart uvicorn.
streamlit not recognized	Activate venv first (.\venv\Scripts\Activate.ps1)
CORS errors	Confirm origins in backend/main.py includes Streamlit origin.
Port already in use	Use --port 8001 for uvicorn, update frontend API URL.
11. Tech Stack

Backend: FastAPI, Python, OpenAI API

Frontend: Streamlit

Libraries: python-dotenv, requests, pydantic, pdfkit, Jinja2

Deployment: Local hackathon/demo