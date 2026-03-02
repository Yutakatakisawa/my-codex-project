export interface PatternWithEmbedding {
  name: string;
  category: string;
  sections: string[];
  description: string;
  embedding?: number[];
}

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

export async function generateEmbedding(text: string): Promise<number[]> {
  if (OPENAI_API_KEY) {
    return generateEmbeddingOpenAI(text);
  }
  if (GEMINI_API_KEY) {
    return generateEmbeddingGemini(text);
  }
  return generateFallbackEmbedding(text);
}

async function generateEmbeddingOpenAI(text: string): Promise<number[]> {
  const OpenAI = (await import("openai")).default;
  const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

  const response = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
  });

  return response.data[0].embedding;
}

async function generateEmbeddingGemini(text: string): Promise<number[]> {
  const { GoogleGenerativeAI } = await import("@google/generative-ai");
  const genAI = new GoogleGenerativeAI(GEMINI_API_KEY!);
  const model = genAI.getGenerativeModel({ model: "embedding-001" });

  const result = await model.embedContent(text);
  return result.embedding.values;
}

function generateFallbackEmbedding(text: string): number[] {
  const words = text.toLowerCase().split(/\s+/);
  const vocab = Array.from(new Set(words));
  const embedding = new Array(384).fill(0);

  vocab.forEach((word, i) => {
    let hash = 0;
    for (let j = 0; j < word.length; j++) {
      hash = (hash << 5) - hash + word.charCodeAt(j);
      hash |= 0;
    }
    const idx = Math.abs(hash) % 384;
    embedding[idx] += 1;
  });

  const norm = Math.sqrt(embedding.reduce((s, v) => s + v * v, 0)) || 1;
  return embedding.map((v) => v / norm);
}

export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) return 0;
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom > 0 ? dot / denom : 0;
}
