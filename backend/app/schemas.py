from pydantic import BaseModel, Field

class InterviewCreate(BaseModel):
    role: str = Field(min_length=2, max_length=100)
    level: str = Field(default="Medium", max_length=50)
    resume_context: str = Field(default="", max_length=5000)
    num_questions: int = Field(default=5, ge=3, le=10)

class InterviewOut(BaseModel):
    id: int
    role: str
    level: str
    questions: list[dict]
    status: str

class EvaluationRequest(BaseModel):
    answers: list[str]

class EvaluationOut(BaseModel):
    interview_id: int
    feedback: dict
