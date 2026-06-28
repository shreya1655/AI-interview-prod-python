"use client";

import { useState } from "react";

const API =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function Home() {
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [questions, setQuestions] = useState<string[]>([]);
  const [error, setError] = useState("");

  async function generateInterview() {
    setLoading(true);
    setError("");
    setQuestions([]);

    try {
      const res = await fetch(`${API}/interviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          role: role || "Software Developer Intern",
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to generate interview");
      }

      const data = await res.json();
      setQuestions(data.questions || []);
    } catch (err) {
      setError("Could not connect to backend. Check API URL.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <section className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">
          AI Mock Interview Platform
        </h1>

        <p className="text-gray-300 mb-8">
          Generate role-based technical interview questions using your deployed
          Python FastAPI backend and Gemini.
        </p>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-lg">
          <label className="block text-sm text-gray-400 mb-2">
            Target Role
          </label>

          <input
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="Software Developer Intern"
            className="w-full rounded-xl bg-gray-800 border border-gray-700 px-4 py-3 text-white outline-none focus:border-blue-500"
          />

          <button
            onClick={generateInterview}
            disabled={loading}
            className="mt-5 rounded-xl bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-700 disabled:opacity-60"
          >
            {loading ? "Generating..." : "Generate Questions"}
          </button>

          {error && (
            <p className="mt-4 text-red-400">
              {error}
            </p>
          )}
        </div>

        {questions.length > 0 && (
          <div className="mt-8 bg-gray-900 border border-gray-800 rounded-2xl p-6">
            <h2 className="text-2xl font-semibold mb-4">
              Interview Questions
            </h2>

            <ol className="space-y-3 list-decimal list-inside text-gray-200">
              {questions.map((q, index) => (
                <li key={index}>{q}</li>
              ))}
            </ol>
          </div>
        )}
      </section>
    </main>
  );
}