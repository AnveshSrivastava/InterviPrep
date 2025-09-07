#!/usr/bin/env python3
"""
Test script for PDF export functionality
Run this after starting the backend server to test the export features
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:8000/interview"

def test_export_functionality():
    """Test the complete export functionality"""
    
    print("🧪 Testing PDF Export Functionality")
    print("=" * 50)
    
    # Step 1: Start a new session
    print("1. Starting new interview session...")
    start_payload = {
        "name": "Test User",
        "role": "Software Engineer",
        "domain": "backend",
        "experience": "1-3 years",
        "mode": "technical"
    }
    
    try:
        response = requests.post(f"{API_BASE}/start", json=start_payload)
        if response.status_code != 200:
            print(f"❌ Failed to start session: {response.text}")
            return False
        
        session_data = response.json()
        session_id = session_data["session_id"]
        questions = session_data["questions"]
        
        print(f"✅ Session started: {session_id}")
        print(f"📝 Generated {len(questions)} questions")
        
    except Exception as e:
        print(f"❌ Error starting session: {str(e)}")
        return False
    
    # Step 2: Submit sample answers
    print("\n2. Submitting sample answers...")
    sample_answers = [
        "I would use a hash table to store the frequency of each character, then iterate through the string to find the first non-repeating character.",
        "I've worked on a microservices architecture where we used Docker containers and Kubernetes for orchestration. We implemented proper service discovery and load balancing.",
        "I would first understand the requirements, then design the database schema, create the API endpoints, and implement proper error handling and validation.",
        "I use Git for version control with feature branches, write unit tests for new code, and follow code review processes to maintain code quality."
    ]
    
    for i, question in enumerate(questions[:len(sample_answers)]):
        answer_payload = {
            "question_id": question["id"],
            "answer": sample_answers[i]
        }
        
        try:
            response = requests.post(f"{API_BASE}/session/{session_id}/answer", json=answer_payload)
            if response.status_code == 200:
                print(f"✅ Answered question {question['id']}")
            else:
                print(f"❌ Failed to answer question {question['id']}: {response.text}")
        except Exception as e:
            print(f"❌ Error answering question {question['id']}: {str(e)}")
    
    # Step 3: Finalize the session
    print("\n3. Finalizing session...")
    try:
        response = requests.post(f"{API_BASE}/session/{session_id}/finalize")
        if response.status_code == 200:
            report_data = response.json()
            print("✅ Session finalized successfully")
            print(f"📊 Overall Score: {report_data.get('overall_score', 'N/A')}/10")
        else:
            print(f"❌ Failed to finalize session: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error finalizing session: {str(e)}")
        return False
    
    # Step 4: Test export endpoints
    print("\n4. Testing export endpoints...")
    
    # Test full report export
    print("📋 Testing full report export...")
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}/export/full")
        if response.status_code == 200:
            print("✅ Full report export successful")
            print(f"📄 PDF size: {len(response.content)} bytes")
        else:
            print(f"❌ Full report export failed: {response.text}")
    except Exception as e:
        print(f"❌ Error exporting full report: {str(e)}")
    
    # Test summary export
    print("📊 Testing summary export...")
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}/export/summary")
        if response.status_code == 200:
            print("✅ Summary export successful")
            print(f"📄 PDF size: {len(response.content)} bytes")
        else:
            print(f"❌ Summary export failed: {response.text}")
    except Exception as e:
        print(f"❌ Error exporting summary: {str(e)}")
    
    # Test base64 exports
    print("🔗 Testing base64 exports...")
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}/export/full/base64")
        if response.status_code == 200:
            pdf_info = response.json()
            print("✅ Base64 full report export successful")
            print(f"📄 Filename: {pdf_info.get('filename', 'N/A')}")
            print(f"📄 Data size: {len(pdf_info.get('pdf_data', ''))} characters")
        else:
            print(f"❌ Base64 full report export failed: {response.text}")
    except Exception as e:
        print(f"❌ Error exporting base64 full report: {str(e)}")
    
    # Test summary base64 export
    try:
        response = requests.get(f"{API_BASE}/session/{session_id}/export/summary/base64")
        if response.status_code == 200:
            pdf_info = response.json()
            print("✅ Base64 summary export successful")
            print(f"📄 Filename: {pdf_info.get('filename', 'N/A')}")
            print(f"📄 Data size: {len(pdf_info.get('pdf_data', ''))} characters")
        else:
            print(f"❌ Base64 summary export failed: {response.text}")
    except Exception as e:
        print(f"❌ Error exporting base64 summary: {str(e)}")
    
    print("\n🎉 Export functionality test completed!")
    return True

if __name__ == "__main__":
    print("Make sure the backend server is running on http://127.0.0.1:8000")
    print("You can start it with: cd backend && uvicorn main:app --reload --port 8000")
    print()
    
    input("Press Enter to start testing...")
    test_export_functionality()
