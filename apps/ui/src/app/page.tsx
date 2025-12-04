import { PageContainer } from "@/components/layout";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <PageContainer>
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h1 className="text-5xl font-bold text-slate-100 mb-4">Geonosis</h1>
        <p className="text-xl text-slate-400 mb-2">
          AI-powered software development orchestration
        </p>
        <p className="text-slate-500 max-w-lg mb-8">
          Transform your ideas into production-ready code. Geonosis uses AI
          agents to analyze requirements, create features, and implement your
          software projects.
        </p>
        <div className="flex gap-4">
          <Button asChild size="lg">
            <Link href="/projects">View Projects</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/projects/new">Create Project</Link>
          </Button>
        </div>
      </div>
    </PageContainer>
  );
}
