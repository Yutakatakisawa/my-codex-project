import type { UIPage, Section } from "@/types/uiSchema";

const COMPONENT_NAMES: Record<string, string> = {
  hero: "Hero",
  features: "Features",
  services: "Services",
  pricing: "Pricing",
  testimonials: "Testimonials",
  contact: "Contact",
  cta: "CTA",
  faq: "FAQ",
};

function escapeString(s: string): string {
  return JSON.stringify(s);
}

function propsToJSX(props: Record<string, unknown>): string {
  if (Object.keys(props).length === 0) return "";
  const entries = Object.entries(props)
    .map(([k, v]) => {
      if (v === undefined || v === null) return null;
      if (typeof v === "string") return `${k}={${escapeString(v)}}`;
      if (typeof v === "number" || typeof v === "boolean") return `${k}={${String(v)}}`;
      return `${k}={${JSON.stringify(v)}}`;
    })
    .filter(Boolean);
  return " " + entries.join(" ");
}

export function exportToReactCode(page: UIPage): string {
  const imports = Array.from(new Set(page.sections.map((s) => COMPONENT_NAMES[s.type] || s.type)))
    .filter(Boolean)
    .sort();

  const importLines = imports
    .map((name) => `import { ${name} } from "@/components/generated/${name}";`)
    .join("\n");

  const sectionLines = page.sections
    .map((section) => {
      const name = COMPONENT_NAMES[section.type] || section.type;
      const propsStr = propsToJSX(section.props as Record<string, unknown>);
      return `      <${name}${propsStr} />`;
    })
    .join("\n");

  return `"use client";

${importLines}

export default function GeneratedPage() {
  return (
    <div className="min-h-screen font-sans">
${sectionLines}
    </div>
  );
}
`;
}
