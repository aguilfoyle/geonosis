import type { Metadata } from "next";

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
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
