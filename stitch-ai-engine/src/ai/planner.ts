import { UIPage } from "@/types/uiSchema";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

const SYSTEM_PROMPT = `You are a UI layout planner. Generate JSON layouts for web pages based on user prompts.
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
Section types: hero, features, services, pricing, testimonials, faq, contact, cta.
Choose sections appropriate for the user's request.`;

export async function planLayout(prompt: string): Promise<UIPage> {
  const userPrompt = `Create a landing page layout JSON for: ${prompt}\n\nOnly return JSON.`;

  if (GEMINI_API_KEY) {
    return planWithGemini(userPrompt);
  }

  if (OPENAI_API_KEY) {
    return planWithOpenAI(userPrompt);
  }

  return getFallbackLayout(prompt);
}

async function planWithGemini(prompt: string): Promise<UIPage> {
  const { GoogleGenerativeAI } = await import("@google/generative-ai");
  const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
  const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

  const result = await model.generateContent([SYSTEM_PROMPT, prompt]);
  const response = result.response;
  const text = response.text();

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

export function parseLayoutResponse(text: string): UIPage {
  const cleaned = text.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
  const parsed = JSON.parse(cleaned) as UIPage;

  if (!parsed.type || !Array.isArray(parsed.sections)) {
    throw new Error("Invalid layout response from AI");
  }

  return {
    type: parsed.type === "dashboard" ? "dashboard" : "landing",
    sections: parsed.sections.map((s) => ({
      type: s.type,
      props: s.props || {},
    })),
  };
}

function getFallbackLayout(prompt: string): UIPage {
  const lower = prompt.toLowerCase();
  const isDashboard = lower.includes("dashboard") || lower.includes("admin");
  const isRoofing = lower.includes("roof") || lower.includes("repair") || lower.includes("contractor");

  if (isRoofing) {
    return {
      type: "landing",
      sections: [
        { type: "hero", props: {} },
        { type: "services", props: {} },
        { type: "testimonials", props: {} },
        { type: "contact", props: {} },
        { type: "cta", props: {} },
      ],
    };
  }

  if (isDashboard) {
    return {
      type: "dashboard",
      sections: [
        { type: "hero", props: {} },
        { type: "features", props: {} },
        { type: "services", props: {} },
      ],
    };
  }

  return {
    type: "landing",
    sections: [
      { type: "hero", props: {} },
      { type: "features", props: {} },
      { type: "pricing", props: {} },
      { type: "testimonials", props: {} },
      { type: "cta", props: {} },
    ],
  };
}
