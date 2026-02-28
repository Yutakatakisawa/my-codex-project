"use client";

export interface HeroProps {
  headline?: string;
  subheadline?: string;
  cta?: { primary?: string; secondary?: string };
  context?: string;
  [key: string]: unknown;
}

export function Hero({ headline, subheadline, cta, ...rest }: HeroProps) {
  const primary = (cta as { primary?: string })?.primary ?? "Get Started";
  const secondary = (cta as { secondary?: string })?.secondary ?? "Learn More";

  return (
    <section className="relative bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white py-24 px-6 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-500/10 via-transparent to-transparent" />
      <div className="relative max-w-5xl mx-auto text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          {headline ?? "Welcome to Our Service"}
        </h1>
        <p className="text-xl md:text-2xl text-slate-300 mb-10 max-w-2xl mx-auto">
          {subheadline ?? "We deliver exceptional results for your business"}
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="px-8 py-4 bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-semibold rounded-lg transition-colors">
            {primary}
          </button>
          <button className="px-8 py-4 border border-slate-500 hover:border-slate-400 text-white font-semibold rounded-lg transition-colors">
            {secondary}
          </button>
        </div>
      </div>
    </section>
  );
}
