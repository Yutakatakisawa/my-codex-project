import type { SectionType } from "@/types/uiSchema";
import type { ComponentType } from "react";

export type SectionComponentMap = Partial<Record<SectionType, ComponentType<Record<string, unknown>>>>;

const registry: SectionComponentMap = {};

export function registerComponent(type: SectionType, component: ComponentType<Record<string, unknown>>): void {
  registry[type] = component;
}

export function getComponent(type: SectionType): ComponentType<Record<string, unknown>> | undefined {
  return registry[type];
}

export function getRegistry(): SectionComponentMap {
  return { ...registry };
}
