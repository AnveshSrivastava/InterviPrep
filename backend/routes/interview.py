from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from uuid import uuid4
from schemas import StartRequest, StartResponse, AnswerRequest
from services.openai_service import generate_questions, evaluate_answer
from services.store import SessionStore
from services.pdf_service import PDFService
import os

router = APIRouter()
store = SessionStore()
pdf_service = PDFService()

@router.post("/start")
async def start(req: StartRequest):
    session_id = str(uuid4())

    # prefer model_provider, fallback to provider (if used elsewhere)
    provider = (req.model_provider or getattr(req, "provider", None) or "gemini").lower()
    api_key = req.api_key or None

    qs = generate_questions(
        req.role, req.domain, req.experience, req.mode, num=4,
        api_key=api_key, provider=provider
    )

    # If service returned an error dict, relay that with 400
    if isinstance(qs, dict) and qs.get("error"):
        raise HTTPException(status_code=400, detail=qs["error"])

    # store meta so evaluation uses same provider/key
    meta = req.dict()
    meta["provider"] = provider

    # Secure handling: don't store raw key, store masked + flag
    if api_key:
        masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
        meta["used_user_key"] = True
        meta["masked_api_key"] = masked_key
    else:
        meta["used_user_key"] = False
        meta["masked_api_key"] = None

    
    store.create(session_id, meta, qs)
    return {"session_id": session_id, "questions": qs}


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    s = store.get(session_id)
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s

@router.post("/session/{session_id}/answer")
async def submit_answer(session_id: str, data: AnswerRequest):
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    q_obj = next((q for q in session["questions"] if q["id"] == data.question_id), None)
    if not q_obj:
        raise HTTPException(status_code=400, detail="Question id not found in session")

    provider = session["meta"].get("provider", "gemini")
    api_key = session["meta"].get("api_key")  # ✅ Allow user key, fallback handled in backend

    eval_res = evaluate_answer(
        q_obj, data.answer,
        session["meta"]["mode"], session["meta"]["experience"],
        api_key=api_key, provider=provider
    )

    # ✅ Fix: use correct variable name and structured error
    if isinstance(eval_res, dict) and eval_res.get("error"):
        raise HTTPException(
            status_code=400,
            detail={
                "message": eval_res["error"],
                "provider": provider,
                "used_user_key": bool(api_key)
            }
        )

    # ✅ Optional: validation guard
    if not isinstance(eval_res, dict):
        raise HTTPException(
            status_code=500,
            detail={"message": "Unexpected evaluation result format", "provider": provider},
        )

    store.save_answer(session_id, {
        "question_id": data.question_id,
        "answer": data.answer,
        "evaluation": eval_res
    })
    return eval_res


    store.save_answer(session_id, {
        "question_id": data.question_id,
        "answer": data.answer,
        "evaluation": eval_res
    })
    return eval_res

@router.post("/session/{session_id}/finalize")
async def finalize(session_id: str):
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    answers = session.get("answers", [])
    if not answers:
        raise HTTPException(status_code=400, detail="No answers provided")
    total_tech = total_comm = total_conf = 0
    resources = []
    for a in answers:
        ev = a["evaluation"]
        sc = ev.get("scores", {})
        total_tech += sc.get("technical", 0)
        total_comm += sc.get("communication", 0)
        total_conf += sc.get("confidence", 0)
        resources += ev.get("resources", []) if ev.get("resources") else []

    n = len(answers)
    avg_tech = round(total_tech / n, 1)
    avg_comm = round(total_comm / n, 1)
    avg_conf = round(total_conf / n, 1)

    mode = session["meta"].get("mode", "technical")
    if mode == "technical":
        overall = round((avg_tech*0.5 + avg_comm*0.25 + avg_conf*0.25), 1)
    else:
        overall = round((avg_comm*0.5 + avg_conf*0.3 + avg_tech*0.2), 1)

    report = {
        "overall_score": overall,
        "avg_technical": avg_tech,
        "avg_communication": avg_comm,
        "avg_confidence": avg_conf,
        "resources": list(dict.fromkeys(resources)),
        "n_questions": n
    }
    store.finalize(session_id, report)
    return report

@router.get("/session/{session_id}/export/full")
async def export_full_report(session_id: str):
    """Export complete interview report as PDF."""
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Session not completed. Please finalize the session first.")
    
    try:
        report_data = session.get("final_report", {})
        pdf_path = pdf_service.generate_interview_report_pdf(session, report_data)
        
        # Get filename from path
        filename = os.path.basename(pdf_path)
        
        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

@router.get("/session/{session_id}/export/summary")
async def export_summary_report(session_id: str):
    """Export interview summary as PDF."""
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Session not completed. Please finalize the session first.")
    
    try:
        report_data = session.get("final_report", {})
        pdf_path = pdf_service.generate_summary_pdf(session, report_data)
        
        # Get filename from path
        filename = os.path.basename(pdf_path)
        
        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

@router.get("/session/{session_id}/export/full/base64")
async def export_full_report_base64(session_id: str):
    """Export complete interview report as base64 encoded PDF."""
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Session not completed. Please finalize the session first.")
    
    try:
        report_data = session.get("final_report", {})
        pdf_path = pdf_service.generate_interview_report_pdf(session, report_data)
        
        # Convert to base64
        pdf_base64 = pdf_service.get_pdf_as_base64(pdf_path)
        filename = os.path.basename(pdf_path)
        
        # Clean up the temporary file
        try:
            os.remove(pdf_path)
        except OSError:
            pass  # File cleanup is not critical
        
        return {
            "filename": filename,
            "pdf_data": pdf_base64,
            "content_type": "application/pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

@router.get("/session/{session_id}/export/summary/base64")
async def export_summary_report_base64(session_id: str):
    """Export interview summary as base64 encoded PDF."""
    session = store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Session not completed. Please finalize the session first.")
    
    try:
        report_data = session.get("final_report", {})
        pdf_path = pdf_service.generate_summary_pdf(session, report_data)
        
        # Convert to base64
        pdf_base64 = pdf_service.get_pdf_as_base64(pdf_path)
        filename = os.path.basename(pdf_path)
        
        # Clean up the temporary file
        try:
            os.remove(pdf_path)
        except OSError:
            pass  # File cleanup is not critical
        
        return {
            "filename": filename,
            "pdf_data": pdf_base64,
            "content_type": "application/pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")