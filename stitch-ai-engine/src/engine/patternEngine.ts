import { retrieveSimilarLayouts } from "@/ai/retrievePatterns";
import type { UIPattern } from "@/ai/retrievePatterns";

export { retrieveSimilarLayouts };
export type { UIPattern };

export function getPatternsByCategory(category: string, patterns: UIPattern[]): UIPattern[] {
  return patterns.filter((p) => p.category === category);
}

export function getPatternsBySection(section: string, patterns: UIPattern[]): UIPattern[] {
  return patterns.filter((p) => p.sections.includes(section));
}
