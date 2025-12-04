import { PageContainer } from "@/components/layout";
import { ProjectActions, StatusBadge, TypeBadge } from "@/components/projects";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { projectsApi } from "@/services/api";
import type { Project } from "@/types";
import Link from "next/link";
import { notFound } from "next/navigation";

interface ProjectPageProps {
  params: Promise<{ id: string }>;
}

/**
 * Format a date string to a readable format.
 */
function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function ProjectPage({ params }: ProjectPageProps) {
  const { id } = await params;

  let project: Project | null = null;

  try {
    project = await projectsApi.get(id);
  } catch {
    notFound();
  }

  if (!project) {
    notFound();
  }

  return (
    <PageContainer>
      {/* Back button */}
      <div className="mb-6">
        <Button asChild variant="ghost" size="sm">
          <Link href="/projects">← Back to Projects</Link>
        </Button>
      </div>

      {/* Header */}
      <div className="flex flex-col gap-4 mb-8">
        <div className="flex items-start justify-between">
          <h1 className="text-3xl font-bold text-slate-100">{project.name}</h1>
          <ProjectActions projectId={id} />
        </div>

        {/* Badges and metadata */}
        <div className="flex items-center gap-4 text-sm">
          <TypeBadge type={project.type} />
          <StatusBadge status={project.status} />
          <Separator orientation="vertical" className="h-4" />
          <span className="text-slate-400">
            Created {formatDate(project.created_at)}
          </span>
          {project.updated_at !== project.created_at && (
            <>
              <Separator orientation="vertical" className="h-4" />
              <span className="text-slate-400">
                Updated {formatDate(project.updated_at)}
              </span>
            </>
          )}
        </div>
      </div>

      {/* GitHub Repository */}
      {project.github_repo_url && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-lg">Repository</CardTitle>
          </CardHeader>
          <CardContent>
            <a
              href={project.github_repo_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 hover:underline"
            >
              {project.github_repo_name || project.github_repo_url}
            </a>
          </CardContent>
        </Card>
      )}

      {/* Epic content */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Epic / Requirements</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="whitespace-pre-wrap font-mono text-sm text-slate-300 bg-slate-900 rounded-lg p-4 overflow-x-auto">
            {project.epic}
          </pre>
        </CardContent>
      </Card>

      {/* Features section placeholder */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle className="text-lg">Features</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-slate-500 text-sm">
            Features will be displayed here once the project is analyzed.
          </p>
        </CardContent>
      </Card>
    </PageContainer>
  );
}
