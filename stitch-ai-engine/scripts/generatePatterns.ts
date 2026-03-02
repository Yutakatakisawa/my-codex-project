/**
 * Generates 1000 UI patterns using AI and saves to src/data/uiPatterns.json
 * Run: npm run generate-patterns
 */

import * as fs from "fs";
import * as path from "path";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

interface UIPattern {
  name: string;
  category: string;
  sections: string[];
  description: string;
}

const SECTION_TYPES = [
  "hero",
  "features",
  "services",
  "pricing",
  "testimonials",
  "faq",
  "contact",
  "cta",
];

const CATEGORIES = [
  "landing",
  "saas",
  "ecommerce",
  "portfolio",
  "agency",
  "dashboard",
  "mobile",
  "admin",
  "blog",
];

function randomChoice<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomSubset<T>(arr: T[], min: number, max: number): T[] {
  const count = min + Math.floor(Math.random() * (max - min + 1));
  const shuffled = [...arr].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, arr.length));
}

async function generateWithAI(batch: number): Promise<UIPattern[]> {
  const count = Math.min(50, 1000 - batch * 50);
  const prompt = `Generate exactly ${count} unique UI layout patterns as JSON array. Each object: { "name": string, "category": string, "sections": string[], "description": string }
Categories: ${CATEGORIES.join(", ")}
Section types: ${SECTION_TYPES.join(", ")}
Make names and descriptions varied and realistic. Return only the JSON array.`;

  if (GEMINI_API_KEY) {
    const { GoogleGenerativeAI } = await import("@google/generative-ai");
    const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(prompt);
    const text = result.response.text();
    return parseAIResponse(text);
  }

  if (OPENAI_API_KEY) {
    const OpenAI = (await import("openai")).default;
    const openai = new OpenAI({ apiKey: OPENAI_API_KEY });
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.9,
    });
    const text = completion.choices[0]?.message?.content ?? "[]";
    return parseAIResponse(text);
  }

  return [];
}

function parseAIResponse(text: string): UIPattern[] {
  const cleaned = text.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
  try {
    const parsed = JSON.parse(cleaned);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function generateSyntheticPatterns(count: number): UIPattern[] {
  const templates = [
    { name: "SaaS", desc: "SaaS marketing page" },
    { name: "E-commerce", desc: "E-commerce product page" },
    { name: "Portfolio", desc: "Creative portfolio" },
    { name: "Agency", desc: "Agency landing page" },
    { name: "Dashboard", desc: "Admin dashboard" },
    { name: "Landing", desc: "Marketing landing page" },
    { name: "Blog", desc: "Blog or content site" },
    { name: "Mobile App", desc: "Mobile app landing" },
    { name: "Service", desc: "Service business page" },
    { name: "Product", desc: "Product showcase" },
  ];

  const patterns: UIPattern[] = [];
  const suffix = ["Pro", "Plus", "Elite", "Standard", "Premium", "Basic", "Starter", "Enterprise"];

  for (let i = 0; i < count; i++) {
    const template = templates[i % templates.length];
    const category = CATEGORIES[i % CATEGORIES.length];
    const sections = randomSubset(SECTION_TYPES, 3, 6);
    patterns.push({
      name: `${template.name} ${suffix[i % suffix.length]} ${i}`,
      category,
      sections,
      description: `${template.desc} for ${category} with ${sections.join(", ")}`,
    });
  }

  return patterns;
}

async function main() {
  const targetCount = 1000;
  let patterns: UIPattern[] = [];

  if (GEMINI_API_KEY || OPENAI_API_KEY) {
    console.log("Using AI to generate patterns...");
    for (let batch = 0; batch < 20; batch++) {
      const batchPatterns = await generateWithAI(batch);
      patterns.push(...batchPatterns);
      console.log(`Batch ${batch + 1}: ${batchPatterns.length} patterns (total: ${patterns.length})`);
      if (patterns.length >= targetCount) break;
      await new Promise((r) => setTimeout(r, 1000));
    }
  }

  if (patterns.length < targetCount) {
    console.log("Filling with synthetic patterns...");
    const synthetic = generateSyntheticPatterns(targetCount - patterns.length);
    patterns.push(...synthetic);
  }

  patterns = patterns.slice(0, targetCount);

  const outputPath = path.join(process.cwd(), "src", "data", "uiPatterns.json");
  fs.writeFileSync(outputPath, JSON.stringify(patterns, null, 2), "utf-8");
  console.log(`Saved ${patterns.length} patterns to ${outputPath}`);
}

main().catch(console.error);
