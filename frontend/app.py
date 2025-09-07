import streamlit as st
import requests
import base64
import io
import json
from datetime import datetime

API = "http://127.0.0.1:8000/interview"

st.set_page_config(page_title="AI Interview Prep", layout="centered")

# Enhanced modern CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        padding: 2rem 0;
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Enhanced Form Styling */
    .form-container {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Enhanced Report Cards */
    .report-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .report-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px -4px rgba(0, 0, 0, 0.15);
    }
    
    /* Enhanced Question Cards */
    .question-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced Feedback Cards */
    .feedback-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #0ea5e9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced Score Badges */
    .score-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        margin: 0.5rem;
        font-size: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .score-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .score-excellent {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        border: 2px solid #22c55e;
    }
    
    .score-good {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        border: 2px solid #3b82f6;
    }
    
    .score-average {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border: 2px solid #f59e0b;
    }
    
    .score-poor {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border: 2px solid #ef4444;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -4px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Enhanced Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #e2e8f0;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Enhanced Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .main-header {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .report-card {
            padding: 1.5rem;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Accessibility */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    /* Focus styles for keyboard navigation */
    button:focus, input:focus, textarea:focus, select:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">AI Interview Prep</h1>', unsafe_allow_html=True)

# Initialize session state
if "session" not in st.session_state:
    st.session_state["session"] = None

# Enhanced form with better styling
st.markdown("""
<div class="form-container">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #1f2937; font-size: 1.75rem;">🎯 Start Your AI-Powered Interview</h2>
    <p style="text-align: center; color: #6b7280; margin-bottom: 2rem; font-size: 1.1rem;">
        Get personalized interview questions and real-time feedback to ace your next interview!
    </p>
</div>
""", unsafe_allow_html=True)

with st.form("start_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Your Name", placeholder="Enter your name")
        role = st.selectbox("💼 Target Role", ["Software Engineer","Product Manager","Data Analyst","UX Designer","DevOps Engineer","Data Scientist","Other"])
        experience = st.selectbox("📈 Experience Level", ["0-1 years","1-3 years","3-5 years","5+ years"])
    
    with col2:
        domain = st.text_input("🔧 Domain (optional)", placeholder="e.g., backend, frontend, ml, cloud")
        mode = st.selectbox("🎯 Interview Mode", ["technical","behavioral","mixed"])
        difficulty = st.selectbox("⚡ Difficulty Level", ["beginner","intermediate","advanced"])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start = st.form_submit_button("🚀 Start Mock Interview", use_container_width=True)

# Start session
if start:
    payload = {
        "name": name or "Anonymous",
        "role": role,
        "domain": domain,
        "experience": experience,
        "mode": mode
    }
    res = requests.post(f"{API}/start", json=payload)
    if res.status_code == 200:
        st.session_state["session"] = res.json()
        st.success("Session started! Scroll down for questions.")
    else:
        st.error("Failed to start session: " + res.text)

# Display questions
if st.session_state["session"]:
    session = st.session_state["session"]
    sid = session["session_id"]
    
    st.markdown("### 💬 Interview Questions")
    
    for q in session["questions"]:
        # Enhanced question display
        st.markdown(f"""
        <div class="question-card">
            <h4 style="color: #1f2937; margin-bottom: 1rem; font-size: 1.25rem;">Question {q['id']}</h4>
            <p style="font-weight: 500; margin-bottom: 1rem; font-size: 1.1rem; line-height: 1.6;">{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        ans_key = f"ans_{q['id']}"
        
        # Enhanced text area
        ans = st.text_area(
            f"✍️ Your answer for Question {q['id']}",
            key=ans_key,
            value=st.session_state.get(ans_key, ""),
            height=150,
            placeholder="Share your thoughts, experiences, or technical knowledge..."
        )
        
        cols = st.columns(3)
        
        # Enhanced buttons with better styling
        if cols[0].button("📤 Submit Answer", key=f"submit_{q['id']}", use_container_width=True):
            if ans.strip():
                with st.spinner("🤖 AI is evaluating your answer..."):
                    payload = {"question_id": q['id'], "answer": ans}
                    resp = requests.post(f"{API}/session/{sid}/answer", json=payload)
                    if resp.status_code == 200:
                        feedback_data = resp.json()
                        
                        # Enhanced feedback display
                        st.markdown(f"""
                        <div class="feedback-card">
                            <h5 style="color: #0ea5e9; margin-bottom: 0.5rem; font-weight: 600;">🤖 AI Feedback</h5>
                            <p style="line-height: 1.6; margin: 0;">{feedback_data.get('feedback', 'Good answer!')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show scores if available
                        if 'scores' in feedback_data:
                            scores = feedback_data['scores']
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Technical", f"{scores.get('technical', 0)}/10")
                            with col2:
                                st.metric("Communication", f"{scores.get('communication', 0)}/10")
                            with col3:
                                st.metric("Confidence", f"{scores.get('confidence', 0)}/10")
                        
                        # Show improvement suggestions
                        if feedback_data.get('examples_or_corrections'):
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #f59e0b; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                                <h5 style="color: #92400e; margin-bottom: 0.5rem; font-weight: 600;">💡 Suggested Improvement</h5>
                                <p style="line-height: 1.6; margin: 0; color: #374151;">{feedback_data['examples_or_corrections']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("❌ Evaluation failed: " + resp.text)
            else:
                st.warning("⚠️ Please provide an answer before submitting.")
        
        # Skip button
        if cols[1].button("⏭️ Skip", key=f"skip_{q['id']}", use_container_width=True):
            st.warning("⏭️ Question skipped.")
        
        # Retry button
        if cols[2].button("🔄 Clear", key=f"retry_{q['id']}", use_container_width=True):
            st.info("🔄 Answer cleared. You can now provide a new answer.")

    # Enhanced finish & report section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 Generate Final Report", use_container_width=True, type="primary"):
            with st.spinner("🤖 Generating your comprehensive interview report..."):
                r = requests.post(f"{API}/session/{sid}/finalize")
                if r.status_code == 200:
                    report_data = r.json()
                    
                    # Store report data in session state for export
                    st.session_state["final_report"] = report_data
                    st.session_state["session_completed"] = True
                    
                    st.success("✅ Final report generated! Scroll down to view your results.")
                    st.rerun()
                else:
                    st.error("❌ Failed to generate report: " + r.text)
    
    # Beautiful Report Display (only show if session is completed)
    if st.session_state.get("session_completed", False):
        report_data = st.session_state.get("final_report", {})
        
        st.markdown("---")
        st.markdown("### 📊 Your Interview Report")
        
        # Report Tabs
        tab1, tab2, tab3 = st.tabs(["📈 Summary", "📋 Detailed Report", "🎯 Actions"])
        
        with tab1:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            
            # Header
            # Get session data from the API response structure
            candidate_name = session.get('name', 'Anonymous')
            role = session.get('role', 'Unknown Role')
            
            st.markdown(f"""
            <div class="section-header">🎯 Interview Summary</div>
            <p style="color: #6b7280; margin-bottom: 2rem; font-size: 1.1rem;">
                <strong>{candidate_name}</strong> • {role} • {datetime.now().strftime('%B %d, %Y')}
            </p>
            """, unsafe_allow_html=True)
            
            # Overall Score
            overall_score = report_data.get('overall_score', 0)
            score_class = "score-excellent" if overall_score >= 8 else "score-good" if overall_score >= 6 else "score-average" if overall_score >= 4 else "score-poor"
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{overall_score:.1f}/10</div>
                    <div class="metric-label">Overall Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed Scores
            st.markdown('<div class="section-header">📊 Performance Breakdown</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                tech_score = report_data.get('avg_technical', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{tech_score:.1f}/10</div>
                    <div class="metric-label">Technical</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                comm_score = report_data.get('avg_communication', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{comm_score:.1f}/10</div>
                    <div class="metric-label">Communication</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                conf_score = report_data.get('avg_confidence', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{conf_score:.1f}/10</div>
                    <div class="metric-label">Confidence</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Session Details
            st.markdown('<div class="section-header">📋 Session Details</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Questions Answered", report_data.get('n_questions', 0))
            with col2:
                st.metric("Interview Mode", session.get('mode', 'technical').title())
            with col3:
                st.metric("Target Role", role)
            
            # Resources
            resources = report_data.get('resources', [])
            if resources:
                st.markdown('<div class="section-header">📚 Recommended Resources</div>', unsafe_allow_html=True)
                for i, resource in enumerate(resources, 1):
                    st.markdown(f"**{i}.** {resource}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            
            # Header
            st.markdown(f"""
            <div class="section-header">📋 Complete Interview Report</div>
            <p style="color: #6b7280; margin-bottom: 2rem; font-size: 1.1rem;">
                <strong>{candidate_name}</strong> • {role} • {session.get('mode', 'technical').title()}
            </p>
            """, unsafe_allow_html=True)
            
            # Questions and Answers
            answers = session.get("answers", [])
            questions = session.get("questions", [])
            
            for answer in answers:
                question = next((q for q in questions if q["id"] == answer["question_id"]), None)
                
                if question:
                    eval_data = answer.get("evaluation", {})
                    scores = eval_data.get("scores", {})
                    
                    # Question Card
                    st.markdown(f"""
                    <div class="question-card">
                        <h4 style="color: #1f2937; margin-bottom: 1rem;">Question {answer['question_id']}</h4>
                        <p style="font-weight: 500; margin-bottom: 1rem;">{question['question']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Answer
                    st.markdown(f"""
                    <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #2563eb;">
                        <strong>Your Answer:</strong><br>
                        <span style="color: #374151;">{answer['answer']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Scores
                    if scores:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Technical", f"{scores.get('technical', 0)}/10")
                        with col2:
                            st.metric("Communication", f"{scores.get('communication', 0)}/10")
                        with col3:
                            st.metric("Confidence", f"{scores.get('confidence', 0)}/10")
                    
                    # Feedback
                    if eval_data.get('feedback'):
                        st.markdown(f"""
                        <div class="feedback-card">
                            <h5 style="color: #0ea5e9; margin-bottom: 0.5rem;">AI Feedback</h5>
                            <p>{eval_data['feedback']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Improvement suggestions
                    if eval_data.get('examples_or_corrections'):
                        st.markdown(f"""
                        <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #f59e0b;">
                            <h5 style="color: #92400e; margin-bottom: 0.5rem;">Suggested Improvement</h5>
                            <p>{eval_data['examples_or_corrections']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 2px solid #e9ecef;'>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="section-header">🎯 What's Next?</div>
            <p style="color: #6b7280; margin-bottom: 2rem; font-size: 1.1rem;">Choose your next action to continue your interview preparation journey</p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📄 Export Your Report")
                if st.button("📥 Download Full Report PDF", help="Download complete report as PDF", use_container_width=True):
                    with st.spinner("📄 Generating PDF..."):
                        try:
                            response = requests.get(f"{API}/session/{sid}/export/full")
                            if response.status_code == 200:
                                pdf_data = response.content
                                filename = f"interview_report_{candidate_name}_{sid[:8]}.pdf"
                                
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=pdf_data,
                                    file_name=filename,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                                st.success("✅ PDF ready for download!")
                            else:
                                st.error("❌ Failed to generate PDF: " + response.text)
                        except Exception as e:
                            st.error(f"❌ Export failed: {str(e)}")
            
            with col2:
                st.markdown("### 🔄 Continue Learning")
                if st.button("🚀 Start New Interview", help="Start a fresh interview session", use_container_width=True, type="primary"):
                    # Clear session state
                    st.session_state["session"] = None
                    st.session_state["final_report"] = None
                    st.session_state["session_completed"] = False
                    st.rerun()
            
            st.markdown("""
            <div style="margin-top: 2rem; padding: 2rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 16px; border-left: 6px solid #0ea5e9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <h4 style="color: #0c4a6e; margin-bottom: 1.5rem; font-size: 1.25rem;">💡 Tips for Continuous Improvement</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                    <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h5 style="color: #667eea; margin-bottom: 0.5rem;">📖 Review & Reflect</h5>
                        <ul style="color: #374151; line-height: 1.6; margin: 0; padding-left: 1.2rem;">
                            <li>Review detailed feedback for each question</li>
                            <li>Identify patterns in your responses</li>
                            <li>Note areas that need more practice</li>
                        </ul>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h5 style="color: #10b981; margin-bottom: 0.5rem;">🎯 Practice & Improve</h5>
                        <ul style="color: #374151; line-height: 1.6; margin: 0; padding-left: 1.2rem;">
                            <li>Practice suggested improvements</li>
                            <li>Focus on areas with lower scores</li>
                            <li>Try different interview modes</li>
                        </ul>
                    </div>
                    <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h5 style="color: #f59e0b; margin-bottom: 0.5rem;">📚 Learn & Grow</h5>
                        <ul style="color: #374151; line-height: 1.6; margin: 0; padding-left: 1.2rem;">
                            <li>Use recommended resources for learning</li>
                            <li>Stay updated with industry trends</li>
                            <li>Build a strong professional network</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)