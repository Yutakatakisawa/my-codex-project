"use client";

export interface ServiceItem {
  title?: string;
  description?: string;
}

export interface ServicesProps {
  title?: string;
  items?: ServiceItem[];
  [key: string]: unknown;
}

export function Services({ title, items = [], ...rest }: ServicesProps) {
  const services = Array.isArray(items) ? items : [];

  return (
    <section className="py-20 px-6 bg-slate-50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-16">
          {title ?? "Our Services"}
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.length > 0 ? (
            services.map((item, i) => (
              <div
                key={i}
                className="p-8 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow"
              >
                <h3 className="text-xl font-semibold text-slate-900 mb-3">
                  {item.title ?? `Service ${i + 1}`}
                </h3>
                <p className="text-slate-600">
                  {item.description ?? "Professional service description"}
                </p>
              </div>
            ))
          ) : (
            <>
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="p-8 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow"
                >
                  <h3 className="text-xl font-semibold text-slate-900 mb-3">
                    Service {i}
                  </h3>
                  <p className="text-slate-600">
                    Professional service description goes here.
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
