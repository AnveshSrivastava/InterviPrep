🤖 InterviewPrepBot

AI-powered mock interview platform. Generate interview questions, submit answers, get real-time AI evaluation, and receive a final report with scores, feedback, and resources. Built with FastAPI backend + Streamlit frontend — fully hackathon-ready.

📂 Project Structure
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

⚡ Features

Dynamic Question Generation: Technical & behavioral questions based on role, domain, and experience.

AI Answer Evaluation:

Scores on Technical, Communication, and Confidence

Actionable Feedback & Improved Examples

Recommended Resources

Final Report: Aggregated scores and insights for review.

Streamlit UI: Interactive, beginner-friendly, hackathon-ready interface.

Fallback Mechanism: Ensures continuous operation even if AI parsing fails.

🚀 Setup Instructions
1. Clone Repository
git clone https://github.com/yourusername/InterviewPrepBot.git
cd InterviewPrepBot

2. Create Python Virtual Environment
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

4. Setup OpenAI API Key
# Copy example .env
cp .env.example backend/.env
# Edit backend/.env
OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY
DEFAULT_MODEL=gpt-3.5-turbo


Alternative: Set system environment variable:

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."

# macOS/Linux
export OPENAI_API_KEY="sk-..."

5. Run Backend
cd backend
uvicorn main:app --reload --port 8000


Open Swagger docs at http://127.0.0.1:8000/docs to inspect API endpoints.

6. Run Frontend
cd frontend
streamlit run app.py


Streamlit will open at http://localhost:8501.

🎯 Using the App

Enter your name, role, domain, experience, and mode (technical/behavioral).

Click Start Mock Interview → questions are generated via AI.

Answer each question → click Submit to get AI evaluation.

Skip or Retry questions if needed.

Click Finish & Get Report → aggregated score and feedback displayed.

🛠 Optional Enhancements

Export final report as PDF (pdfkit + Jinja2).

Voice input using OpenAI Whisper.

Persist sessions in SQLite.

Visual improvements in Streamlit UI.

🔧 Troubleshooting
Error	Fix
OPENAI_API_KEY not found	Ensure backend/.env exists & API key is valid. Restart uvicorn.
streamlit not recognized	Activate venv first (.\venv\Scripts\Activate.ps1).
CORS errors	Confirm allowed origins in backend/main.py.
Port already in use	Use --port 8001 for uvicorn & update frontend API URL.
🏗 Tech Stack

Backend: FastAPI, Python, OpenAI API

Frontend: Streamlit

Libraries: python-dotenv, requests, pydantic, pdfkit, Jinja2

Deployment: Local hackathon/demo-ready