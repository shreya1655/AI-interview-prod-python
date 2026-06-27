"use client";
import { useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Question = { id: number; question: string; topic: string };

export default function Home() {
  const [role, setRole] = useState("SDE Intern");
  const [level, setLevel] = useState("Medium");
  const [resumeContext, setResumeContext] = useState("");
  const [interviewId, setInterviewId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<string[]>([]);
  const [feedback, setFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const userId = typeof window !== "undefined" ? localStorage.getItem("demoUserId") || "demo-user" : "demo-user";

  async function startInterview() {
    setLoading(true); setFeedback(null);
    try {
      const res = await fetch(`${API}/interviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-User-Id": userId },
        body: JSON.stringify({ role, level, resume_context: resumeContext, num_questions: 5 })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setInterviewId(data.id); setQuestions(data.questions); setAnswers(Array(data.questions.length).fill(""));
    } catch (e:any) { alert(e.message); }
    finally { setLoading(false); }
  }

  async function evaluate() {
    if (!interviewId) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/interviews/${interviewId}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-User-Id": userId },
        body: JSON.stringify({ answers })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json(); setFeedback(data.feedback);
    } catch (e:any) { alert(e.message); }
    finally { setLoading(false); }
  }

  return <main className="container">
    <h1>AI Mock Interview Platform</h1>
    <p className="muted">Python FastAPI backend + batched 5-question interview + one final Gemini evaluation.</p>
    <section className="card">
      <div className="grid">
        <label>Role<input value={role} onChange={e=>setRole(e.target.value)} /></label>
        <label>Level<select value={level} onChange={e=>setLevel(e.target.value)}><option>Easy</option><option>Medium</option><option>Hard</option></select></label>
      </div>
      <label>Resume / project context<textarea rows={4} value={resumeContext} onChange={e=>setResumeContext(e.target.value)} placeholder="Paste project/resume context here" /></label>
      <button disabled={loading} onClick={startInterview}>{loading ? "Generating..." : "Generate 5-question Interview"}</button>
    </section>

    {questions.length > 0 && <section className="card">
      <h2>Interview Questions</h2>
      {questions.map((q, i) => <div className="question" key={q.id || i}>
        <b>Q{i+1}. {q.question}</b><p className="muted">Topic: {q.topic}</p>
        <textarea rows={5} value={answers[i]} onChange={e => { const next=[...answers]; next[i]=e.target.value; setAnswers(next); }} placeholder="Write or paste your answer..." />
      </div>)}
      <button disabled={loading || answers.some(a=>!a.trim())} onClick={evaluate}>{loading ? "Evaluating..." : "Submit all answers for feedback"}</button>
    </section>}

    {feedback && <section className="card">
      <h2>Feedback</h2>
      <div className="score">{feedback.overallScore}/100</div>
      <p><b>Technical Depth:</b> {feedback.technicalDepth}/100</p>
      <p><b>Communication:</b> {feedback.communication}/100</p>
      <pre>{JSON.stringify(feedback, null, 2)}</pre>
    </section>}
  </main>;
}
