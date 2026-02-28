import patterns from "./uiPatterns.json";

export type UIPattern = {
  name: string;
  category: string;
  sections: string[];
  description: string;
};

export const uiPatterns = patterns as UIPattern[];
