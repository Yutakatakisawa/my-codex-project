"use client";

export interface ContactProps {
  title?: string;
  fields?: string[];
  submitText?: string;
  [key: string]: unknown;
}

export function Contact({
  title,
  fields = ["name", "email", "message"],
  submitText = "Send Message",
  ...rest
}: ContactProps) {
  const formFields = Array.isArray(fields) ? fields : ["name", "email", "message"];

  return (
    <section className="py-20 px-6 bg-white">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-slate-900 text-center mb-12">
          {title ?? "Get In Touch"}
        </h2>
        <form className="space-y-6">
          {formFields.includes("name") && (
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-slate-700 mb-2"
              >
                Name
              </label>
              <input
                id="name"
                type="text"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                placeholder="Your name"
              />
            </div>
          )}
          {formFields.includes("email") && (
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-slate-700 mb-2"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                placeholder="your@email.com"
              />
            </div>
          )}
          {formFields.includes("message") && (
            <div>
              <label
                htmlFor="message"
                className="block text-sm font-medium text-slate-700 mb-2"
              >
                Message
              </label>
              <textarea
                id="message"
                rows={5}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                placeholder="Your message..."
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full py-4 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold rounded-lg transition-colors"
          >
            {submitText}
          </button>
        </form>
      </div>
    </section>
  );
}
