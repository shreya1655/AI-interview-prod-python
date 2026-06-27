# AI Interview Platform — Python Backend Production Starter

A production-oriented mock interview platform for 50 interviews/day.

## Architecture

- Frontend: Next.js
- Backend: Python FastAPI
- AI: Gemini API
- DB: SQLite locally, Postgres/Supabase-ready through `DATABASE_URL`
- Scaling design: one API call generates 5 questions, one API call evaluates all answers

## Features

- Generate 5 interview questions in one Gemini call
- Submit all answers together for one final feedback call
- Store interview history in database
- Daily global limit: default 50 interviews/day
- Daily per-user limit: default 5 interviews/day
- CORS configured for local frontend
- Ready to migrate from demo `X-User-Id` to real Supabase/Clerk auth

## Run backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# add GEMINI_API_KEY in .env
uvicorn app.main:app --reload --port 8000
```

Open API docs: http://localhost:8000/docs

## Run frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open: http://localhost:3000

## Production deployment idea

- Deploy frontend on Vercel
- Deploy backend on Render/Railway/Fly.io
- Use Supabase Postgres as database
- Replace demo `X-User-Id` with real JWT auth
- Set `DAILY_GLOBAL_LIMIT=50` and `DAILY_USER_LIMIT=3` or `5`

## Resume-safe bullet

Engineered a Python FastAPI-backed AI mock interview platform with batched 5-question generation, one-shot feedback evaluation, persistent interview storage and daily rate limits supporting 50+ interview sessions/day.
