import { generateEmbedding, cosineSimilarity } from "./embedding";
import { uiPatterns } from "@/data/patterns";

export interface UIPattern {
  name: string;
  category: string;
  sections: string[];
  description: string;
}

export interface PatternWithScore extends UIPattern {
  score: number;
}

const EMBEDDINGS_CACHE_KEY = "ui-pattern-embeddings";

async function loadPatternsWithEmbeddings(): Promise<Array<UIPattern & { embedding: number[] }>> {
  const patterns = uiPatterns;

  if (typeof window !== "undefined") {
    const cached = localStorage.getItem(EMBEDDINGS_CACHE_KEY);
    if (cached) {
      try {
        return JSON.parse(cached);
      } catch {
        // invalid cache
      }
    }
  }

  const withEmbeddings = await Promise.all(
    patterns.map(async (p) => {
      const text = `${p.name} ${p.category} ${p.sections.join(" ")} ${p.description}`;
      const embedding = await generateEmbedding(text);
      return { ...p, embedding };
    })
  );

  if (typeof window !== "undefined") {
    try {
      localStorage.setItem(EMBEDDINGS_CACHE_KEY, JSON.stringify(withEmbeddings));
    } catch {
      // quota exceeded
    }
  }

  return withEmbeddings;
}

let serverEmbeddingsCache: Array<UIPattern & { embedding: number[] }> | null = null;

export async function retrieveSimilarLayouts(prompt: string, topK = 5): Promise<PatternWithScore[]> {
  const patterns = await (typeof window === "undefined"
    ? (async () => {
        if (serverEmbeddingsCache) return serverEmbeddingsCache;
        const { uiPatterns: patterns } = await import("@/data/patterns");
        const withEmbeddings = await Promise.all(
          patterns.map(async (p) => {
            const text = `${p.name} ${p.category} ${p.sections.join(" ")} ${p.description}`;
            const embedding = await generateEmbedding(text);
            return { ...p, embedding };
          })
        );
        serverEmbeddingsCache = withEmbeddings;
        return withEmbeddings;
      })()
    : loadPatternsWithEmbeddings());

  const promptEmbedding = await generateEmbedding(prompt);

  const scored = patterns.map((p) => ({
    ...p,
    score: cosineSimilarity(p.embedding, promptEmbedding),
  }));

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK).map(({ embedding: _, ...rest }) => rest);
}
