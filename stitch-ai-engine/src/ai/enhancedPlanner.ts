import { UIPage } from "@/types/uiSchema";
import { retrieveSimilarLayouts } from "./retrievePatterns";
import { planLayout, parseLayoutResponse } from "./planner";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

const SYSTEM_PROMPT = `You are a UI layout planner. Generate JSON layouts for web pages based on user prompts and relevant UI patterns.
Only return valid JSON. No markdown, no code blocks, no explanation.
Follow this exact schema:
{
  "type": "landing" | "dashboard",
  "sections": [
    {
      "type": "hero" | "features" | "services" | "pricing" | "testimonials" | "faq" | "contact" | "cta",
      "props": {}
    }
  ]
}
Use the relevant patterns as inspiration but adapt to the user's specific request.`;

export async function planLayoutWithRAG(prompt: string): Promise<UIPage> {
  if (!GEMINI_API_KEY && !OPENAI_API_KEY) {
    return planLayout(prompt);
  }

  const patterns = await retrieveSimilarLayouts(prompt, 5);

  const patternsContext = patterns
    .map(
      (p) =>
        `- ${p.name} (${p.category}): ${p.sections.join(" → ")} - ${p.description}`
    )
    .join("\n");

  const userPrompt = `User request: ${prompt}

Relevant UI patterns:
${patternsContext}

Generate UI layout JSON that best fits the user's request. Only return JSON.`;

  if (GEMINI_API_KEY) {
    return planWithGemini(userPrompt);
  }

  if (OPENAI_API_KEY) {
    return planWithOpenAI(userPrompt);
  }

  return planLayout(prompt);
}

async function planWithGemini(prompt: string): Promise<UIPage> {
  const { GoogleGenerativeAI } = await import("@google/generative-ai");
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
  const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

  const result = await model.generateContent([SYSTEM_PROMPT, prompt]);
  const text = result.response.text();
  return parseLayoutResponse(text);
}

async function planWithOpenAI(prompt: string): Promise<UIPage> {
  const OpenAI = (await import("openai")).default;
  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: prompt },
    ],
    temperature: 0.7,
  });

  const text = completion.choices[0]?.message?.content ?? "";
  return parseLayoutResponse(text);
}
