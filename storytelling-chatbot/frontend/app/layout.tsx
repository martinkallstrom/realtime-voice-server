import React from "react";

import "./globals.css";

import type { Metadata } from "next";
import { Space_Grotesk, Space_Mono } from "next/font/google";

// Font
const sans = Space_Grotesk({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-sans",
});

const mono = Space_Mono({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Storytelling Chatbot - Daily AI",
  description: "Built with git.new/ai",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${sans.variable} ${mono.variable} flex flex-col min-h-screen p-6`}
      >
        <main className="flex flex-1">{children}</main>
        <footer className="flex-0 text-center font-mono text-xs text-gray-500">
          Created with{" "}
          <a
            href="https://git.new/ai"
            className="text-violet-700 underline decoration-violet-200"
          >
            git.new/ai
          </a>
        </footer>
      </body>
    </html>
  );
}
