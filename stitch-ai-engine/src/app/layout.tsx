import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Stitch AI Engine",
  description: "AI-powered UI layout generation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
