"use client";

import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Fixed header component for the application.
 */
export function Header() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === "/") {
      return pathname === "/";
    }
    return pathname.startsWith(href);
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-slate-900 border-b border-slate-800">
      <div className="h-full max-w-7xl mx-auto px-4 flex items-center justify-between">
        {/* Logo / Title */}
        <Link
          href="/"
          className="text-xl font-bold text-white hover:text-slate-200 transition-colors"
        >
          Geonosis
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-6">
          <Link
            href="/projects"
            className={cn(
              "text-sm font-medium transition-colors hover:text-white",
              isActive("/projects") ? "text-white" : "text-slate-400"
            )}
          >
            Projects
          </Link>
          <Link
            href="/projects/new"
            className={cn(
              "text-sm font-medium px-3 py-1.5 rounded-md transition-colors",
              "bg-primary text-primary-foreground hover:bg-primary/90"
            )}
          >
            New Project
          </Link>
        </nav>
      </div>
    </header>
  );
}
