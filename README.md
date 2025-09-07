# 🤖 AI Interview Prep Bot

> **An LLM-powered chatbot that simulates technical and behavioral interviews for job seekers**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange.svg)](https://ai.google.dev)

## 🎯 Problem Statement

The goal is to build an LLM-based chatbot that can simulate technical or behavioral interviews for job seekers. This tool should not only ask relevant questions based on the chosen role but also evaluate the candidate's responses, offering feedback, scoring, and suggestions for improvement.

## ✨ Key Features & Implementation Status

### ✅ **Fully Implemented Features**

#### 🎭 **User Role & Domain Selection**
- ✅ User chooses target job role (Software Engineer, Product Manager, Data Analyst, etc.)
- ✅ Optional domain specification (frontend, backend, ML, system design)
- ✅ Experience level selection (0-1 years, 1-3 years, 3-5 years, 5+ years)

#### 🎯 **Interview Mode Selection**
- ✅ **Technical Interview**: Algorithm questions, coding, system design, domain-specific
- ✅ **Behavioral Interview**: STAR-format questions, teamwork, leadership, conflict resolution
- ✅ **Mixed Mode**: Combination of both technical and behavioral questions

#### 🤖 **AI-Powered Question Generation**
- ✅ Dynamic question generation using Google Gemini AI
- ✅ Role-specific and domain-specific question customization
- ✅ Experience-level appropriate difficulty scaling
- ✅ Fallback mechanism for robust operation

#### 💬 **Simulated Conversation Flow**
- ✅ Smooth Q&A format with 4 questions per session
- ✅ Real-time answer submission and evaluation
- ✅ Skip and retry functionality for each question
- ✅ Session state management

#### 🧠 **AI Answer Evaluation**
- ✅ **Multi-dimensional Scoring**:
  - Technical Accuracy (1-10)
  - Communication Skills (1-10) 
  - Confidence & Structure (1-10)
- ✅ **Comprehensive Feedback**:
  - Actionable improvement suggestions
  - Real-world examples and corrections
  - STAR format guidance for behavioral questions
- ✅ **Resource Recommendations**: Curated learning materials and links

#### 📊 **Final Summary Report**
- ✅ **Performance Analytics**:
  - Overall weighted score calculation
  - Detailed breakdown by category
  - Session statistics and insights
- ✅ **Actionable Insights**:
  - Areas of strength identification
  - Improvement recommendations
  - Personalized resource suggestions

#### 🎨 **Modern Web Interface**
- ✅ **Streamlit Frontend**: Clean, responsive, and user-friendly
- ✅ **Professional Styling**: Modern CSS with gradients and animations
- ✅ **Interactive Elements**: Real-time feedback, progress tracking
- ✅ **Mobile Responsive**: Optimized for all device sizes

#### 📄 **PDF Export Functionality**
- ✅ **Full Report Export**: Complete interview with all Q&A and feedback
- ✅ **Summary Export**: Concise performance overview
- ✅ **Base64 Export**: Web-friendly PDF delivery
- ✅ **Professional Formatting**: ReportLab-generated professional PDFs

### 🏗️ **Technical Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │  Google Gemini  │
│   Frontend      │◄──►│   Backend       │◄──►│      AI API     │
│                 │    │                 │    │                 │
│ • User Interface│    │ • REST API      │    │ • Question Gen  │
│ • Session Mgmt  │    │ • Session Store │    │ • Answer Eval   │
│ • PDF Export    │    │ • PDF Service   │    │ • Feedback Gen  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📂 **Project Structure**
```
InterviPrep/
├── backend/                    # FastAPI Backend
│   ├── main.py                # FastAPI app with CORS
│   ├── routes/
│   │   └── interview.py       # Interview API endpoints
│   ├── services/
│   │   ├── openai_service.py  # Google Gemini AI integration
│   │   ├── store.py          # In-memory session storage
│   │   └── pdf_service.py    # PDF generation service
│   ├── schemas.py            # Pydantic data models
│   └── templates/            # PDF templates (auto-created)
├── frontend/
│   └── app.py                # Streamlit frontend application
├── exports/                  # Generated PDF reports (auto-created)
├── requirements.txt          # Python dependencies
├── test_export.py           # Export functionality testing
├── EXPORT_SETUP.md          # PDF export setup guide
└── README.md                # This file
```

## 🚀 Quick Start Guide

### 1. **Clone Repository**
```bash
git clone https://github.com/yourusername/InterviPrep.git
cd InterviPrep
```

### 2. **Setup Python Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. **Configure Google Gemini API**
Create a `.env` file in the `backend/` directory:
```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_MODEL=gemini-1.5-flash
```

**Alternative**: Set system environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_gemini_api_key_here"

# macOS/Linux
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 4. **Start the Application**

**Terminal 1 - Backend Server:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
📖 **API Documentation**: http://127.0.0.1:8000/docs

**Terminal 2 - Frontend Interface:**
```bash
cd frontend
streamlit run app.py
```
🌐 **Web Interface**: http://localhost:8501

## 🎯 How to Use

### **Step 1: Start Your Interview**
1. Enter your **name**, **target role**, and **domain** (optional)
2. Select your **experience level** and **interview mode**
3. Click **"🚀 Start Mock Interview"**

### **Step 2: Answer Questions**
1. Read each AI-generated question carefully
2. Provide your answer in the text area
3. Click **"📤 Submit Answer"** for AI evaluation
4. Review feedback, scores, and improvement suggestions
5. Use **"⏭️ Skip"** or **"🔄 Clear"** as needed

### **Step 3: Get Your Report**
1. Click **"📊 Generate Final Report"** after answering questions
2. View your **overall performance** and **detailed breakdown**
3. **Download PDF reports** for future reference
4. Start a **new interview session** to practice more

## 🛠️ **Advanced Features**

### **PDF Export Options**
- **📄 Full Report**: Complete interview with all Q&A and feedback
- **📊 Summary Report**: Concise performance overview
- **🔗 Base64 Export**: Web-friendly PDF delivery
- **🖨️ Print-Friendly**: Browser-based PDF viewing

### **API Endpoints**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/interview/start` | POST | Start new interview session |
| `/interview/session/{id}/answer` | POST | Submit answer for evaluation |
| `/interview/session/{id}/finalize` | POST | Generate final report |
| `/interview/session/{id}/export/full` | GET | Download complete PDF report |
| `/interview/session/{id}/export/summary` | GET | Download summary PDF |

## 🔧 **Troubleshooting**

| Issue | Solution |
|-------|----------|
| **GEMINI_API_KEY not found** | Ensure `backend/.env` exists with valid API key. Restart uvicorn. |
| **streamlit not recognized** | Activate virtual environment first: `.\venv\Scripts\Activate.ps1` |
| **CORS errors** | Confirm allowed origins in `backend/main.py` |
| **Port already in use** | Use `--port 8001` for uvicorn & update frontend API URL |
| **PDF export fails** | Check `exports/` directory permissions and ReportLab installation |

## 🏗️ **Tech Stack**

### **Backend**
- **FastAPI**: Modern, fast web framework for building APIs
- **Google Gemini AI**: Advanced LLM for question generation and evaluation
- **ReportLab**: Professional PDF generation
- **Pydantic**: Data validation and serialization

### **Frontend**
- **Streamlit**: Rapid web app development framework
- **Modern CSS**: Responsive design with animations
- **Real-time Updates**: Dynamic session management

### **Additional Libraries**
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API communication
- **uuid**: Session ID generation

## 🎯 **Requirements Fulfillment Analysis**

### ✅ **Core Requirements Met**

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| **User Role & Domain Selection** | ✅ Complete | Dropdown selection with 7+ roles, optional domain input |
| **Interview Mode Selection** | ✅ Complete | Technical, Behavioral, and Mixed modes |
| **Simulated Conversation** | ✅ Complete | 4-question Q&A format with real-time evaluation |
| **AI Answer Evaluation** | ✅ Complete | 3-dimensional scoring (Technical, Communication, Confidence) |
| **Real-Time Interaction** | ✅ Complete | Skip, retry, and smooth conversation flow |
| **Final Summary Report** | ✅ Complete | Comprehensive analytics with actionable insights |
| **Web UI** | ✅ Complete | Modern Streamlit interface with professional styling |
| **Export Functionality** | ✅ Complete | PDF export with multiple format options |

### 🚀 **Bonus Features Implemented**

| Feature | Status | Description |
|---------|--------|-------------|
| **PDF Export** | ✅ Complete | Full and summary reports with professional formatting |
| **Session Management** | ✅ Complete | In-memory storage with session persistence |
| **Responsive Design** | ✅ Complete | Mobile-optimized interface |
| **Error Handling** | ✅ Complete | Graceful fallbacks and user-friendly error messages |
| **API Documentation** | ✅ Complete | Auto-generated Swagger/OpenAPI docs |

## 🧪 **Testing**

### **Manual Testing**
1. Start both backend and frontend servers
2. Complete a full interview session
3. Test all export functionality
4. Verify PDF generation and download

### **Automated Testing**
```bash
# Run the export functionality test
python test_export.py
```

## 🚀 **Deployment Ready**

This application is **hackathon-ready** and can be deployed to:
- **Local Development**: Already configured
- **Cloud Platforms**: Heroku, Railway, Render
- **Container Deployment**: Docker-ready architecture
- **Production**: Scalable FastAPI + Streamlit setup

## 📈 **Future Enhancements**

### **Potential Improvements**
- [ ] **Voice Integration**: Speech-to-text and text-to-speech
- [ ] **Database Persistence**: SQLite/PostgreSQL for session storage
- [ ] **User Authentication**: Login system with progress tracking
- [ ] **Custom Question Sets**: FAANG-style, company-specific questions
- [ ] **Leaderboard**: Gamified scoring and competition
- [ ] **Multi-language Support**: Internationalization
- [ ] **Advanced Analytics**: Performance trends and insights

---

## 📞 **Support**

For issues, questions, or contributions:
- 📧 **Email**: [your-email@domain.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/InterviPrep/issues)
- 📖 **Documentation**: See `EXPORT_SETUP.md` for detailed setup guide

---

**🎉 Ready to ace your next interview? Start practicing with AI Interview Prep Bot!**