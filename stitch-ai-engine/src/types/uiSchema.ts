import { z } from "zod";

export const SectionTypeSchema = z.enum([
  "hero",
  "features",
  "services",
  "pricing",
  "testimonials",
  "faq",
  "contact",
  "cta",
]);

export const SectionSchema = z.object({
  type: SectionTypeSchema,
  props: z.record(z.unknown()),
});

export const UIPageSchema = z.object({
  type: z.enum(["landing", "dashboard"]),
  sections: z.array(SectionSchema),
});

export type SectionType = z.infer<typeof SectionTypeSchema>;
export type Section = z.infer<typeof SectionSchema>;
export type UIPage = z.infer<typeof UIPageSchema>;

export function validateUIPage(data: unknown): UIPage {
  return UIPageSchema.parse(data);
}

export function safeValidateUIPage(data: unknown): { success: true; data: UIPage } | { success: false; error: z.ZodError } {
  const result = UIPageSchema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, error: result.error };
}
