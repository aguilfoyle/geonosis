import { PageContainer } from "@/components/layout";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function ProjectNotFound() {
  return (
    <PageContainer>
      <div className="flex flex-col items-center justify-center py-16 text-center">
        <h1 className="text-4xl font-bold text-slate-100 mb-4">
          Project Not Found
        </h1>
        <p className="text-slate-400 mb-8 max-w-md">
          The project you&apos;re looking for doesn&apos;t exist or may have
          been deleted.
        </p>
        <Button asChild>
          <Link href="/projects">Back to Projects</Link>
        </Button>
      </div>
    </PageContainer>
  );
}
