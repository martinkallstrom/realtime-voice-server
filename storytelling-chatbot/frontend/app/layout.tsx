import React from "react";

import "./globals.css";
import type { Metadata } from "next";
import { Space_Grotesk, Space_Mono } from "next/font/google";

import { cn } from "@/lib/utils";

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
        className={cn(
          "min-h-screen bg-background font-sans antialiased flex flex-col",
          sans.variable,
          mono.variable
        )}
      >
        <main className="flex flex-1 items-center">{children}</main>
        <footer className="flex-0 text-center font-mono text-sm text-gray-100 py-6">
          <span className="bg-gray-800/70 px-3 py-1 rounded-md">
            Created with{" "}
            <a
              href="https://git.new/ai"
              className="text-violet-300 underline decoration-violet-400 hover:text-violet-100"
            >
              git.new/ai
            </a>
          </span>
        </footer>
      </body>
    </html>
  );
}
