"use client";

export interface FAQItem {
  question?: string;
  answer?: string;
}

export interface FAQProps {
  title?: string;
  items?: FAQItem[];
  [key: string]: unknown;
}

export function FAQ({ title, items = [], ...rest }: FAQProps) {
  const faqItems = Array.isArray(items) ? items : [];

  return (
    <section className="py-20 px-6 bg-slate-50">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-12">
          {title ?? "Frequently Asked Questions"}
        </h2>
        <div className="space-y-4">
          {faqItems.length > 0 ? (
            faqItems.map((item, i) => (
              <details
                key={i}
                className="p-4 bg-white rounded-lg border border-slate-200"
              >
                <summary className="font-semibold text-slate-900 cursor-pointer">
                  {item.question ?? `Question ${i + 1}`}
                </summary>
                <p className="mt-2 text-slate-600">{item.answer ?? "Answer"}</p>
              </details>
            ))
          ) : (
            <>
              <details className="p-4 bg-white rounded-lg border border-slate-200">
                <summary className="font-semibold text-slate-900 cursor-pointer">
                  How does it work?
                </summary>
                <p className="mt-2 text-slate-600">We provide a simple process.</p>
              </details>
              <details className="p-4 bg-white rounded-lg border border-slate-200">
                <summary className="font-semibold text-slate-900 cursor-pointer">
                  What are the costs?
                </summary>
                <p className="mt-2 text-slate-600">Transparent pricing available.</p>
              </details>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
