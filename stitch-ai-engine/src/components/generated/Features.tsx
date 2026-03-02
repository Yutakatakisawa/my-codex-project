"use client";

export interface FeatureItem {
  title?: string;
  description?: string;
}

export interface FeaturesProps {
  title?: string;
  items?: FeatureItem[];
  [key: string]: unknown;
}

export function Features({ title, items = [], ...rest }: FeaturesProps) {
  const features = Array.isArray(items) ? items : [];

  return (
    <section className="py-20 px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-16">
          {title ?? "Key Features"}
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.length > 0 ? (
            features.map((item, i) => (
              <div
                key={i}
                className="p-6 rounded-xl border border-slate-200 hover:border-cyan-300 hover:shadow-lg transition-all"
              >
                <h3 className="text-xl font-semibold text-slate-900 mb-2">
                  {item.title ?? `Feature ${i + 1}`}
                </h3>
                <p className="text-slate-600">
                  {item.description ?? "Description of this feature"}
                </p>
              </div>
            ))
          ) : (
            <>
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="p-6 rounded-xl border border-slate-200 hover:border-cyan-300 hover:shadow-lg transition-all"
                >
                  <h3 className="text-xl font-semibold text-slate-900 mb-2">
                    Feature {i}
                  </h3>
                  <p className="text-slate-600">
                    Description of the feature goes here.
                  </p>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </section>
  );
}
