"use client";

import { useState } from "react";
import { RenderPage } from "@/renderer/RenderPage";
import type { UIPage } from "@/types/uiSchema";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [page, setPage] = useState<UIPage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setPage(null);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || `HTTP ${res.status}`);
      }

      const data: UIPage = await res.json();
      setPage(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-slate-900">
            Stitch AI Engine
          </h1>
          <p className="text-slate-600 text-sm mt-1">
            Generate UI layouts from prompts
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-8">
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Describe the layout you want
          </label>
          <div className="flex gap-3">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
              placeholder="e.g. Landing page for roofing repair company"
              className="flex-1 px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
            />
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 disabled:bg-slate-400 text-white font-semibold rounded-lg transition-colors"
            >
              {loading ? "Generating…" : "Generate"}
            </button>
          </div>
          {error && (
            <p className="mt-2 text-red-600 text-sm">{error}</p>
          )}
        </div>

        {page && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-slate-900">
              Live Preview
            </h2>
            <div className="rounded-xl overflow-hidden border border-slate-200 bg-white shadow-sm">
              <RenderPage page={page} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
