"use client";

export interface PricingPlan {
  name?: string;
  price?: string;
  features?: string[];
}

export interface PricingProps {
  title?: string;
  plans?: PricingPlan[];
  [key: string]: unknown;
}

export function Pricing({ title, plans = [], ...rest }: PricingProps) {
  const pricingPlans = Array.isArray(plans) ? plans : [];

  return (
    <section className="py-20 px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-16">
          {title ?? "Pricing Plans"}
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {pricingPlans.length > 0 ? (
            pricingPlans.map((plan, i) => (
              <div
                key={i}
                className={`p-8 rounded-xl border-2 ${
                  i === 1
                    ? "border-cyan-500 shadow-lg scale-105 bg-cyan-50/50"
                    : "border-slate-200"
                }`}
              >
                <h3 className="text-xl font-semibold text-slate-900 mb-2">
                  {plan.name ?? `Plan ${i + 1}`}
                </h3>
                <p className="text-3xl font-bold text-slate-900 mb-4">
                  {plan.price ?? "$0"}
                </p>
                <ul className="space-y-2 text-slate-600">
                  {(plan.features ?? []).map((f, j) => (
                    <li key={j} className="flex items-center gap-2">
                      <span className="text-cyan-500">✓</span> {f}
                    </li>
                  ))}
                </ul>
                <button
                  className={`mt-6 w-full py-3 rounded-lg font-semibold transition-colors ${
                    i === 1
                      ? "bg-cyan-500 text-white hover:bg-cyan-600"
                      : "bg-slate-100 text-slate-900 hover:bg-slate-200"
                  }`}
                >
                  Choose Plan
                </button>
              </div>
            ))
          ) : (
            <>
              {["Basic", "Pro", "Enterprise"].map((name, i) => (
                <div
                  key={i}
                  className={`p-8 rounded-xl border-2 ${
                    i === 1
                      ? "border-cyan-500 shadow-lg scale-105 bg-cyan-50/50"
                      : "border-slate-200"
                  }`}
                >
                  <h3 className="text-xl font-semibold text-slate-900 mb-2">
                    {name}
                  </h3>
                  <p className="text-3xl font-bold text-slate-900 mb-4">
                    ${[29, 79, 199][i]}
                  </p>
                  <ul className="space-y-2 text-slate-600">
                    <li className="flex items-center gap-2">
                      <span className="text-cyan-500">✓</span> Feature 1
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-cyan-500">✓</span> Feature 2
                    </li>
                  </ul>
                  <button
                    className={`mt-6 w-full py-3 rounded-lg font-semibold ${
                      i === 1 ? "bg-cyan-500 text-white" : "bg-slate-100 text-slate-900"
                    }`}
                  >
                    Choose Plan
                  </button>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </section>
  );
}
