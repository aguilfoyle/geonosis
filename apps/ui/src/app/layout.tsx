import { Header } from "@/components/layout";
import { ToastProvider } from "@/components/providers";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Geonosis",
  description: "AI-powered software development orchestration",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <Header />
        <main className="pt-16">{children}</main>
        <ToastProvider />
      </body>
    </html>
  );
}
