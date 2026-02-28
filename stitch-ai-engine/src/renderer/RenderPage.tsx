"use client";

import type { UIPage, Section } from "@/types/uiSchema";
import { Hero } from "@/components/generated/Hero";
import { Features } from "@/components/generated/Features";
import { Services } from "@/components/generated/Services";
import { Pricing } from "@/components/generated/Pricing";
import { Testimonials } from "@/components/generated/Testimonials";
import { Contact } from "@/components/generated/Contact";
import { CTA } from "@/components/generated/CTA";
import { FAQ } from "@/components/generated/FAQ";

const ComponentMap: Record<string, React.ComponentType<Record<string, unknown>>> = {
  hero: Hero as React.ComponentType<Record<string, unknown>>,
  features: Features as React.ComponentType<Record<string, unknown>>,
  services: Services as React.ComponentType<Record<string, unknown>>,
  pricing: Pricing as React.ComponentType<Record<string, unknown>>,
  testimonials: Testimonials as React.ComponentType<Record<string, unknown>>,
  contact: Contact as React.ComponentType<Record<string, unknown>>,
  cta: CTA as React.ComponentType<Record<string, unknown>>,
  faq: FAQ as React.ComponentType<Record<string, unknown>>,
};

export function RenderPage({ page }: { page: UIPage }) {
  return (
    <div className="min-h-screen font-sans">
      {page.sections.map((section, index) => (
        <SectionRenderer key={`${section.type}-${index}`} section={section} />
      ))}
    </div>
  );
}

function SectionRenderer({ section }: { section: Section }) {
  const Component = ComponentMap[section.type];

  if (!Component) {
    return (
      <div className="p-8 bg-amber-50 border border-amber-200 rounded-lg m-4">
        <p className="text-amber-800 font-medium">Unknown section type: {section.type}</p>
      </div>
    );
  }

  return <Component {...(section.props as Record<string, unknown>)} />;
}
