from datetime import datetime, timezone, time
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import ApiEvent, Interview
from .schemas import EvaluationOut, EvaluationRequest, InterviewCreate, InterviewOut
from .gemini import generate_questions, evaluate_answers

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Interview Platform API")

origins = [o.strip() for o in settings.allowed_origins.split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def start_of_today():
    now = datetime.now(timezone.utc)
    return datetime.combine(now.date(), time.min, tzinfo=timezone.utc)

def check_limits(db: Session, user_id: str):
    since = start_of_today()
    global_count = db.query(func.count(ApiEvent.id)).filter(ApiEvent.event_type == "interview_created", ApiEvent.created_at >= since).scalar()
    user_count = db.query(func.count(ApiEvent.id)).filter(ApiEvent.user_id == user_id, ApiEvent.event_type == "interview_created", ApiEvent.created_at >= since).scalar()
    if global_count >= settings.daily_global_limit:
        raise HTTPException(429, "Daily platform interview limit reached. Try tomorrow.")
    if user_count >= settings.daily_user_limit:
        raise HTTPException(429, "Your daily interview limit is reached. Try tomorrow.")

def current_user(x_user_id: str | None = Header(default=None)):
    return x_user_id or "demo-user"

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/interviews", response_model=InterviewOut)
async def create_interview(payload: InterviewCreate, db: Session = Depends(get_db), user_id: str = Depends(current_user)):
    check_limits(db, user_id)
    try:
        questions = await generate_questions(payload.role, payload.level, payload.resume_context, payload.num_questions)
    except Exception as e:
        raise HTTPException(502, f"AI question generation failed: {str(e)}")
    interview = Interview(user_id=user_id, role=payload.role, level=payload.level, questions=questions, status="generated")
    db.add(interview)
    db.add(ApiEvent(user_id=user_id, event_type="interview_created"))
    db.commit()
    db.refresh(interview)
    return interview

@app.post("/interviews/{interview_id}/evaluate", response_model=EvaluationOut)
async def evaluate_interview(interview_id: int, payload: EvaluationRequest, db: Session = Depends(get_db), user_id: str = Depends(current_user)):
    interview = db.query(Interview).filter(Interview.id == interview_id, Interview.user_id == user_id).first()
    if not interview:
        raise HTTPException(404, "Interview not found")
    if len(payload.answers) != len(interview.questions):
        raise HTTPException(400, "Number of answers must match number of questions")
    try:
        feedback = await evaluate_answers(interview.role, interview.level, interview.questions, payload.answers)
    except Exception as e:
        raise HTTPException(502, f"AI feedback generation failed: {str(e)}")
    interview.answers = payload.answers
    interview.feedback = feedback
    interview.status = "evaluated"
    db.add(ApiEvent(user_id=user_id, event_type="interview_evaluated"))
    db.commit()
    return {"interview_id": interview.id, "feedback": feedback}

@app.get("/interviews")
def list_interviews(db: Session = Depends(get_db), user_id: str = Depends(current_user)):
    rows = db.query(Interview).filter(Interview.user_id == user_id).order_by(Interview.created_at.desc()).limit(20).all()
    return rows

@app.get("/usage/today")
def usage_today(db: Session = Depends(get_db), user_id: str = Depends(current_user)):
    since = start_of_today()
    global_count = db.query(func.count(ApiEvent.id)).filter(ApiEvent.event_type == "interview_created", ApiEvent.created_at >= since).scalar()
    user_count = db.query(func.count(ApiEvent.id)).filter(ApiEvent.user_id == user_id, ApiEvent.event_type == "interview_created", ApiEvent.created_at >= since).scalar()
    return {"global_interviews_today": global_count, "user_interviews_today": user_count, "global_limit": settings.daily_global_limit, "user_limit": settings.daily_user_limit}
