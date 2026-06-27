import json
import re
import httpx
from .config import settings

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

async def call_gemini(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")
    url = GEMINI_URL.format(model=settings.gemini_model, key=settings.gemini_api_key)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 2048}
    }
    async with httpx.AsyncClient(timeout=45) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def parse_json(text: str):
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)

async def generate_questions(role: str, level: str, resume_context: str, n: int):
    prompt = f"""
You are an interview coach. Generate exactly {n} interview questions for a {level} {role} candidate.
Use the resume/project context only if useful: {resume_context}
Return ONLY valid JSON in this format:
{{"questions":[{{"id":1,"question":"...","topic":"..."}}]}}
No markdown.
"""
    return parse_json(await call_gemini(prompt))["questions"]

async def evaluate_answers(role: str, level: str, questions: list, answers: list[str]):
    qa = [{"question": q.get("question", ""), "answer": answers[i] if i < len(answers) else ""} for i, q in enumerate(questions)]
    prompt = f"""
Evaluate this {level} {role} mock interview.
Question-answer pairs: {json.dumps(qa)}
Return ONLY valid JSON:
{{
  "overallScore": 0,
  "technicalDepth": 0,
  "communication": 0,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "questionWiseFeedback": [{{"questionId":1,"score":0,"feedback":"...","improvedAnswer":"..."}}],
  "finalAdvice": "..."
}}
Scores must be 0-100. No markdown.
"""
    return parse_json(await call_gemini(prompt))
