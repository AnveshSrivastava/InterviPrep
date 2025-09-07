# 🏗️ AI Interview Prep Bot - System Architecture

## 📋 Overview

The AI Interview Prep Bot follows a **3-tier architecture** with clear separation of concerns:

1. **Presentation Layer** (Streamlit Frontend)
2. **Business Logic Layer** (FastAPI Backend) 
3. **External Services Layer** (Google Gemini AI)

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Streamlit Frontend                       │   │
│  │  • User Input Forms    • Real-time Feedback            │   │
│  │  • Session Management  • PDF Export Interface          │   │
│  │  • Modern UI/UX        • Mobile Responsive Design      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/REST API
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                FastAPI Backend                          │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │   │
│  │  │   Routes    │ │  Services   │ │   Schemas   │      │   │
│  │  │             │ │             │ │             │      │   │
│  │  │• Interview  │ │• AI Service │ │• Data Models│      │   │
│  │  │• Session    │ │• PDF Service│ │• Validation │      │   │
│  │  │• Export     │ │• Store      │ │• Serialize  │      │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ API Calls
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Google Gemini AI API                       │   │
│  │  • Question Generation  • Answer Evaluation            │   │
│  │  • Feedback Creation    • Resource Recommendations     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    User     │    │  Streamlit  │    │   FastAPI   │    │   Gemini    │
│             │    │  Frontend   │    │   Backend   │    │     AI      │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       │ 1. Fill Form      │                   │                   │
       ├──────────────────►│                   │                   │
       │                   │ 2. POST /start    │                   │
       │                   ├──────────────────►│                   │
       │                   │                   │ 3. Generate Qs   │
       │                   │                   ├──────────────────►│
       │                   │                   │ 4. Questions     │
       │                   │                   │◄──────────────────┤
       │                   │ 5. Questions      │                   │
       │                   │◄──────────────────┤                   │
       │ 6. Display Qs     │                   │                   │
       │◄──────────────────┤                   │                   │
       │                   │                   │                   │
       │ 7. Submit Answer  │                   │                   │
       ├──────────────────►│                   │                   │
       │                   │ 8. POST /answer   │                   │
       │                   ├──────────────────►│                   │
       │                   │                   │ 9. Evaluate      │
       │                   │                   ├──────────────────►│
       │                   │                   │ 10. Feedback     │
       │                   │                   │◄──────────────────┤
       │                   │ 11. Feedback      │                   │
       │                   │◄──────────────────┤                   │
       │ 12. Show Results  │                   │                   │
       │◄──────────────────┤                   │                   │
       │                   │                   │                   │
       │ 13. Finalize      │                   │                   │
       ├──────────────────►│                   │                   │
       │                   │ 14. POST /finalize│                   │
       │                   ├──────────────────►│                   │
       │                   │ 15. Report        │                   │
       │                   │◄──────────────────┤                   │
       │ 16. Show Report   │                   │                   │
       │◄──────────────────┤                   │                   │
```

## 🏛️ Component Architecture

### 1. **Frontend Layer (Streamlit)**

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Session   │  │    UI       │  │   Export    │        │
│  │ Management  │  │ Components  │  │ Interface   │        │
│  │             │  │             │  │             │        │
│  │• State Mgmt │  │• Forms      │  │• PDF Download│       │
│  │• API Calls  │  │• Feedback   │  │• Base64 Export│      │
│  │• Validation │  │• Styling    │  │• Print View  │       │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Key Components:**
- **Session State Management**: Tracks user progress and session data
- **Form Components**: User input forms with validation
- **Feedback Display**: Real-time AI feedback and scoring
- **Export Interface**: PDF download and print functionality
- **Responsive Design**: Mobile-optimized CSS styling

### 2. **Backend Layer (FastAPI)**

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Routes   │  │  Services   │  │   Schemas   │        │
│  │             │  │             │  │             │        │
│  │• /start     │  │• AI Service │  │• StartRequest│       │
│  │• /answer    │  │• PDF Service│  │• AnswerRequest│      │
│  │• /finalize  │  │• Store      │  │• EvalResponse│       │
│  │• /export    │  │• Validation │  │• Question   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Route Structure:**
```
/interview/
├── POST /start                    # Initialize new session
├── GET /session/{id}              # Get session details
├── POST /session/{id}/answer      # Submit answer for evaluation
├── POST /session/{id}/finalize    # Generate final report
├── GET /session/{id}/export/full  # Download complete PDF
├── GET /session/{id}/export/summary # Download summary PDF
├── GET /session/{id}/export/full/base64    # Base64 full report
└── GET /session/{id}/export/summary/base64 # Base64 summary
```

### 3. **Service Layer Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ AI Service  │  │ PDF Service │  │Store Service│        │
│  │             │  │             │  │             │        │
│  │• Question   │  │• Report Gen │  │• Session    │        │
│  │  Generation │  │• Template   │  │  Storage    │        │
│  │• Answer     │  │  Engine     │  │• State Mgmt │        │
│  │  Evaluation │  │• Base64     │  │• Cleanup    │        │
│  │• Feedback   │  │  Encoding   │  │• Persistence│        │
│  │  Creation   │  │• File Mgmt  │  │• Validation │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 🗄️ Data Architecture

### **Session Data Model**

```python
Session = {
    "session_id": "uuid4",
    "meta": {
        "name": "string",
        "role": "string", 
        "domain": "string",
        "experience": "string",
        "mode": "technical|behavioral|mixed"
    },
    "questions": [
        {
            "id": "int",
            "question": "string",
            "type": "string",
            "difficulty": "string",
            "hint": "string"
        }
    ],
    "answers": [
        {
            "question_id": "int",
            "answer": "string",
            "evaluation": {
                "scores": {
                    "technical": "int (1-10)",
                    "communication": "int (1-10)", 
                    "confidence": "int (1-10)"
                },
                "feedback": "string",
                "examples_or_corrections": "string",
                "resources": ["string"]
            }
        }
    ],
    "final_report": {
        "overall_score": "float",
        "avg_technical": "float",
        "avg_communication": "float", 
        "avg_confidence": "float",
        "resources": ["string"],
        "n_questions": "int"
    },
    "created_at": "timestamp",
    "status": "ongoing|completed"
}
```

### **API Request/Response Models**

```python
# Request Models
StartRequest = {
    "name": "string",
    "role": "string",
    "domain": "string (optional)",
    "experience": "string",
    "mode": "string"
}

AnswerRequest = {
    "question_id": "int",
    "answer": "string"
}

# Response Models
StartResponse = {
    "session_id": "string",
    "questions": [Question]
}

EvalResponse = {
    "question_id": "int",
    "scores": {"technical": int, "communication": int, "confidence": int},
    "feedback": "string",
    "examples_or_corrections": "string (optional)",
    "resources": ["string (optional)"]
}
```

## 🔧 Technical Implementation Details

### **AI Integration Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                Google Gemini AI Integration                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Question    │  │ Answer      │  │ Error       │        │
│  │ Generation  │  │ Evaluation  │  │ Handling    │        │
│  │             │  │             │  │             │        │
│  │• Role-based │  │• Multi-dim  │  │• Fallback   │        │
│  │• Domain     │  │  Scoring    │  │  Questions  │        │
│  │  Specific   │  │• Feedback   │  │• Default    │        │
│  │• Experience │  │  Generation │  │  Responses  │        │
│  │  Level      │  │• Resource   │  │• Graceful   │        │
│  │• Difficulty │  │  Suggestions│  │  Degradation│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**AI Service Features:**
- **Prompt Engineering**: Structured prompts for consistent output
- **JSON Parsing**: Safe parsing with fallback mechanisms
- **Error Handling**: Graceful degradation when AI fails
- **Rate Limiting**: Built-in API call management
- **Caching**: Session-based response caching

### **PDF Generation Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    PDF Service Architecture                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Template    │  │ Content     │  │ File        │        │
│  │ Engine      │  │ Generation  │  │ Management  │        │
│  │             │  │             │  │             │        │
│  │• ReportLab  │  │• Data       │  │• Auto-cleanup│       │
│  │• Styling    │  │  Binding    │  │• Unique     │        │
│  │• Layout     │  │• Formatting │  │  Filenames  │        │
│  │• Typography │  │• Tables     │  │• Base64     │        │
│  │• Colors     │  │• Charts     │  │  Encoding   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**PDF Features:**
- **Professional Styling**: Custom fonts, colors, and layouts
- **Dynamic Content**: Session-specific data binding
- **Multiple Formats**: Full report, summary, and base64 export
- **File Management**: Automatic cleanup and unique naming
- **Error Handling**: Graceful fallbacks for generation failures

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layer                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Input       │  │ API         │  │ Data        │        │
│  │ Validation  │  │ Security    │  │ Protection  │        │
│  │             │  │             │  │             │        │
│  │• Pydantic   │  │• CORS       │  │• Session    │        │
│  │  Models     │  │  Headers    │  │  Isolation  │        │
│  │• Sanitization│  │• Rate      │  │• No PII     │        │
│  │• Type       │  │  Limiting   │  │  Storage    │        │
│  │  Checking   │  │• Error      │  │• Temporary  │        │
│  │• Length     │  │  Handling   │  │  Files      │        │
│  │  Limits     │  │• Logging    │  │• Cleanup    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Security Features:**
- **Input Validation**: Pydantic models for all API inputs
- **CORS Protection**: Configured allowed origins
- **Session Isolation**: UUID-based session management
- **No Persistent Storage**: In-memory only, no database
- **File Cleanup**: Automatic removal of temporary files
- **Error Sanitization**: Safe error messages without sensitive data

## 🚀 Deployment Architecture

### **Local Development**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Browser   │    │  Streamlit  │    │   FastAPI   │
│             │    │  (Port 8501)│    │  (Port 8000)│
│• localhost  │◄──►│             │◄──►│             │
│• 8501       │    │• Frontend   │    │• Backend    │
│             │    │• UI/UX      │    │• API        │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Production Deployment Options**

#### **Option 1: Cloud Platform (Heroku/Railway)**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Users     │    │   Cloud     │    │   Gemini    │
│             │    │  Platform   │    │     AI      │
│• Web        │◄──►│             │◄──►│             │
│• Mobile     │    │• FastAPI    │    │• API        │
│             │    │• Streamlit  │    │• External   │
└─────────────┘    └─────────────┘    └─────────────┘
```

#### **Option 2: Container Deployment (Docker)**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Users     │    │   Docker    │    │   Gemini    │
│             │    │  Container  │    │     AI      │
│• Web        │◄──►│             │◄──►│             │
│• Mobile     │    │• App Bundle │    │• API        │
│             │    │• Services   │    │• External   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 📊 Performance Architecture

### **Scalability Considerations**

```
┌─────────────────────────────────────────────────────────────┐
│                Performance Optimization                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Caching     │  │ Async       │  │ Resource    │        │
│  │ Strategy    │  │ Processing  │  │ Management  │        │
│  │             │  │             │  │             │        │
│  │• Session    │  │• AI Calls   │  │• Memory     │        │
│  │  Storage    │  │• PDF Gen    │  │  Usage      │        │
│  │• Response   │  │• File I/O   │  │• CPU        │        │
│  │  Caching    │  │• Database   │  │  Optimization│       │
│  │• API        │  │  Queries    │  │• File       │        │
│  │  Throttling │  │• Background │  │  Cleanup    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Performance Features:**
- **In-Memory Storage**: Fast session access
- **Async Operations**: Non-blocking AI calls
- **File Cleanup**: Automatic temporary file removal
- **Response Caching**: Reduced API calls
- **Error Recovery**: Graceful degradation

## 🔄 State Management Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                State Management Flow                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Frontend  │    │   Backend   │    │   External  │    │
│  │   State     │    │   State     │    │   Services  │    │
│  │             │    │             │    │             │    │
│  │• Session    │◄──►│• Session    │◄──►│• AI State   │    │
│  │  Data       │    │  Store      │    │• API Keys   │    │
│  │• UI State   │    │• Memory     │    │• Rate Limits│    │
│  │• Form Data  │    │• Validation │    │• Responses  │    │
│  │• Progress   │    │• Cleanup    │    │• Caching    │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Decisions

### **1. Technology Choices**
- **FastAPI**: High-performance async API framework
- **Streamlit**: Rapid prototyping and deployment
- **Google Gemini**: Advanced LLM capabilities
- **ReportLab**: Professional PDF generation
- **Pydantic**: Type-safe data validation

### **2. Design Patterns**
- **3-Tier Architecture**: Clear separation of concerns
- **Service Layer Pattern**: Business logic encapsulation
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: PDF generation flexibility
- **Observer Pattern**: Real-time UI updates

### **3. Scalability Considerations**
- **Stateless Backend**: Easy horizontal scaling
- **In-Memory Storage**: Fast access, suitable for demo
- **Async Operations**: Non-blocking I/O
- **File Cleanup**: Automatic resource management
- **Error Handling**: Graceful degradation

## 📈 Future Architecture Enhancements

### **Phase 1: Database Integration**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Backend   │    │  Database   │
│             │    │             │    │             │
│• Streamlit  │◄──►│• FastAPI    │◄──►│• PostgreSQL │
│• UI/UX      │    │• Services   │    │• Sessions   │
│             │    │• ORM        │    │• Users      │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Phase 2: Microservices Architecture**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │    │   Gateway   │    │  Services   │
│             │    │             │    │             │
│• Streamlit  │◄──►│• API        │◄──►│• Interview  │
│• UI/UX      │    │  Gateway    │    │• AI         │
│             │    │• Load       │    │• PDF        │
│             │    │  Balancer   │    │• Auth       │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Phase 3: Cloud-Native Architecture**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CDN       │    │   Cloud     │    │   External  │
│             │    │  Platform   │    │  Services   │
│• Static     │◄──►│             │◄──►│             │
│  Assets     │    │• Containers │    │• AI APIs    │
│• Caching    │    │• Auto-scaling│   │• Storage    │
│• Global     │    │• Monitoring │    │• Analytics  │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

This architecture provides a solid foundation for the AI Interview Prep Bot while maintaining flexibility for future enhancements and scaling requirements.
