"use client";

import { useState } from "react";
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

interface RenderPageProps {
  page: UIPage;
  draggable?: boolean;
  onReorder?: (from: number, to: number) => void;
}

export function RenderPage({ page, draggable, onReorder }: RenderPageProps) {
  const [dragOver, setDragOver] = useState<number | null>(null);

  function handleDragStart(e: React.DragEvent, index: number) {
    e.dataTransfer.setData("text/plain", String(index));
    e.dataTransfer.effectAllowed = "move";
  }

  function handleDragOver(e: React.DragEvent, index: number) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    setDragOver(index);
  }

  function handleDragLeave() {
    setDragOver(null);
  }

  function handleDrop(e: React.DragEvent, toIndex: number) {
    e.preventDefault();
    setDragOver(null);
    const fromIndex = parseInt(e.dataTransfer.getData("text/plain"), 10);
    if (!isNaN(fromIndex) && onReorder) {
      onReorder(fromIndex, toIndex);
    }
  }

  return (
    <div className="min-h-screen font-sans">
      {page.sections.map((section, index) => (
        <div
          key={`${section.type}-${index}`}
          onDragOver={(e) => draggable && handleDragOver(e, index)}
          onDragLeave={handleDragLeave}
          onDrop={(e) => draggable && handleDrop(e, index)}
          className={`relative group ${dragOver === index ? "ring-2 ring-cyan-500 ring-inset" : ""}`}
        >
          {draggable && (
            <div
              draggable
              onDragStart={(e) => handleDragStart(e, index)}
              className="absolute left-2 top-2 z-10 opacity-0 group-hover:opacity-100 transition-opacity cursor-grab active:cursor-grabbing p-2 bg-white/90 rounded border border-slate-300 shadow-sm"
              title="Drag to reorder"
            >
              <svg className="w-4 h-4 text-slate-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M7 2a1 1 0 011 1v1h3V3a1 1 0 112 0v1h3a1 1 0 110 2h-3v1a1 1 0 11-2 0V6H8v1a1 1 0 01-2 0V4a1 1 0 011-1z" />
                <path d="M3 8a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
                <path d="M3 12a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
              </svg>
            </div>
          )}
          <SectionRenderer section={section} />
        </div>
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
