"use client";

export interface TestimonialItem {
  quote?: string;
  author?: string;
  role?: string;
}

export interface TestimonialsProps {
  title?: string;
  items?: TestimonialItem[];
  [key: string]: unknown;
}

export function Testimonials({ title, items = [], ...rest }: TestimonialsProps) {
  const testimonials = Array.isArray(items) ? items : [];

  return (
    <section className="py-20 px-6 bg-slate-50">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-16">
          {title ?? "What Our Customers Say"}
        </h2>
        <div className="grid md:grid-cols-2 gap-8">
          {testimonials.length > 0 ? (
            testimonials.map((item, i) => (
              <blockquote
                key={i}
                className="p-8 bg-white rounded-xl shadow-sm border-l-4 border-cyan-500"
              >
                <p className="text-slate-700 text-lg mb-4">
                  &ldquo;{item.quote ?? "Great service!"}&rdquo;
                </p>
                <footer>
                  <cite className="font-semibold text-slate-900 not-italic">
                    {item.author ?? "Customer"}
                  </cite>
                  {item.role && (
                    <span className="text-slate-500 text-sm ml-2">
                      — {item.role}
                    </span>
                  )}
                </footer>
              </blockquote>
            ))
          ) : (
            <>
              <blockquote className="p-8 bg-white rounded-xl shadow-sm border-l-4 border-cyan-500">
                <p className="text-slate-700 text-lg mb-4">
                  &ldquo;Excellent service! Highly recommended.&rdquo;
                </p>
                <footer>
                  <cite className="font-semibold text-slate-900 not-italic">
                    Jane Doe
                  </cite>
                  <span className="text-slate-500 text-sm ml-2">— CEO</span>
                </footer>
              </blockquote>
              <blockquote className="p-8 bg-white rounded-xl shadow-sm border-l-4 border-cyan-500">
                <p className="text-slate-700 text-lg mb-4">
                  &ldquo;Outstanding results. Will use again.&rdquo;
                </p>
                <footer>
                  <cite className="font-semibold text-slate-900 not-italic">
                    John Smith
                  </cite>
                  <span className="text-slate-500 text-sm ml-2">— Founder</span>
                </footer>
              </blockquote>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
