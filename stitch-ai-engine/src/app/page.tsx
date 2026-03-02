"use client";

import { useState } from "react";
import { RenderPage } from "@/renderer/RenderPage";
import { exportToReactCode } from "@/engine/codeExporter";
import type { UIPage, Section } from "@/types/uiSchema";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [page, setPage] = useState<UIPage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);

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

  function handleExportCode() {
    if (!page) return;
    setShowCode(true);
  }

  async function handleCopyCode() {
    if (!page) return;
    const code = exportToReactCode(page);
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function handleReorder(from: number, to: number) {
    if (!page || from === to) return;
    const sections = [...page.sections];
    const [removed] = sections.splice(from, 1);
    sections.splice(to, 0, removed);
    setPage({ ...page, sections });
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
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-900">
                Live Preview
              </h2>
              <div className="flex gap-2">
                <button
                  onClick={handleExportCode}
                  className="px-4 py-2 text-sm bg-slate-200 hover:bg-slate-300 text-slate-800 font-medium rounded-lg transition-colors"
                >
                  Export React Code
                </button>
              </div>
            </div>
            <div className="rounded-xl overflow-hidden border border-slate-200 bg-white shadow-sm">
              <RenderPage page={page} onReorder={handleReorder} draggable />
            </div>
          </div>
        )}
      </main>

      {showCode && page && (
        <CodeModal
          code={exportToReactCode(page)}
          onClose={() => setShowCode(false)}
          onCopy={handleCopyCode}
          copied={copied}
        />
      )}
    </div>
  );
}

function CodeModal({
  code,
  onClose,
  onCopy,
  copied,
}: {
  code: string;
  onClose: () => void;
  onCopy: () => void;
  copied: boolean;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div className="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900">React Code Export</h3>
          <div className="flex gap-2">
            <button
              onClick={onCopy}
              className="px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-white text-sm font-medium rounded-lg"
            >
              {copied ? "Copied!" : "Copy"}
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 text-sm font-medium rounded-lg"
            >
              Close
            </button>
          </div>
        </div>
        <pre className="p-4 overflow-auto flex-1 text-sm bg-slate-900 text-slate-100 rounded-b-xl">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
}
