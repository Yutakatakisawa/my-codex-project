import { UIPage } from "@/types/uiSchema";
import { validateUIPage } from "@/types/uiSchema";
import { planLayoutWithRAG } from "@/ai/enhancedPlanner";
import { expandAllSections } from "@/ai/componentGenerator";

export async function generateLayout(prompt: string): Promise<UIPage> {
  const rawLayout = await planLayoutWithRAG(prompt);
  const validated = validateUIPage(rawLayout);
  const expanded = {
    ...validated,
    sections: expandAllSections(validated.sections, prompt),
  };
  return expanded;
}
