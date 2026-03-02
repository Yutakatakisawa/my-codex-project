"use client";

export interface CTAProps {
  headline?: string;
  subheadline?: string;
  buttonText?: string;
  [key: string]: unknown;
}

export function CTA({
  headline,
  subheadline,
  buttonText = "Sign Up Now",
  ...rest
}: CTAProps) {
  return (
    <section className="py-20 px-6 bg-gradient-to-r from-cyan-600 to-cyan-700 text-white">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          {headline ?? "Ready to Get Started?"}
        </h2>
        <p className="text-xl text-cyan-100 mb-8">
          {subheadline ?? "Join thousands of satisfied customers"}
        </p>
        <button className="px-10 py-4 bg-white text-cyan-600 font-semibold rounded-lg hover:bg-cyan-50 transition-colors">
          {buttonText}
        </button>
      </div>
    </section>
  );
}
