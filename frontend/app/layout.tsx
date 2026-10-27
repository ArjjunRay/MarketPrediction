import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "QStream | Quantitative Research Terminal",
  description:
    "Real-time, entitlement-aware quantitative market research platform.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">
          Skip to main content
        </a>
        {children}
      </body>
    </html>
  );
}
