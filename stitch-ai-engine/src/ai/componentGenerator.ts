import { Section, SectionType } from "@/types/uiSchema";

const DEFAULT_CONTENT: Record<SectionType, Record<string, unknown>> = {
  hero: {
    headline: "Welcome to Our Service",
    subheadline: "We deliver exceptional results for your business",
    cta: { primary: "Get Started", secondary: "Learn More" },
  },
  features: {
    title: "Key Features",
    items: [
      { title: "Feature One", description: "Description of the first feature" },
      { title: "Feature Two", description: "Description of the second feature" },
      { title: "Feature Three", description: "Description of the third feature" },
    ],
  },
  services: {
    title: "Our Services",
    items: [
      { title: "Service One", description: "Professional service description" },
      { title: "Service Two", description: "Professional service description" },
      { title: "Service Three", description: "Professional service description" },
    ],
  },
  pricing: {
    title: "Pricing Plans",
    plans: [
      { name: "Basic", price: "$29", features: ["Feature 1", "Feature 2"] },
      { name: "Pro", price: "$79", features: ["Feature 1", "Feature 2", "Feature 3"] },
      { name: "Enterprise", price: "$199", features: ["All features", "Priority support"] },
    ],
  },
  testimonials: {
    title: "What Our Customers Say",
    items: [
      { quote: "Excellent service!", author: "Jane Doe", role: "CEO" },
      { quote: "Highly recommended.", author: "John Smith", role: "Founder" },
    ],
  },
  faq: {
    title: "Frequently Asked Questions",
    items: [
      { question: "How does it work?", answer: "We provide a simple process." },
      { question: "What are the costs?", answer: "Transparent pricing available." },
    ],
  },
  contact: {
    title: "Get In Touch",
    fields: ["name", "email", "message"],
    submitText: "Send Message",
  },
  cta: {
    headline: "Ready to Get Started?",
    subheadline: "Join thousands of satisfied customers",
    buttonText: "Sign Up Now",
  },
};

export function expandSectionContent(section: Section, context?: string): Section {
  const defaults = DEFAULT_CONTENT[section.type];
  const merged = { ...defaults, ...section.props };

  if (context) {
    merged.context = context;
  }

  return {
    type: section.type,
    props: merged,
  };
}

export function expandAllSections(
  sections: Section[],
  context?: string
): Section[] {
  return sections.map((s) => expandSectionContent(s, context));
}
