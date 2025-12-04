import { PageContainer } from "@/components/layout";
import { StatusBadge, TypeBadge } from "@/components/projects";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { projectsApi } from "@/services/api";
import type { ProjectListItem } from "@/types";
import Link from "next/link";

/**
 * Format a date string to a readable format.
 */
function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default async function ProjectsPage() {
  let projects: ProjectListItem[] = [];
  let error: string | null = null;

  try {
    projects = await projectsApi.list();
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load projects";
  }

  return (
    <PageContainer
      title="Projects"
      description="Manage your AI-powered development projects"
    >
      {/* Header with Create button */}
      <div className="flex justify-between items-center mb-8">
        <div />
        <Button asChild>
          <Link href="/projects/new">Create Project</Link>
        </Button>
      </div>

      {/* Error state */}
      {error && (
        <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300">
          <p>Error: {error}</p>
          <p className="text-sm text-red-400 mt-2">
            Make sure the API server is running at http://localhost:8000
          </p>
        </div>
      )}

      {/* Empty state */}
      {!error && projects.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <h3 className="text-xl font-semibold text-slate-300 mb-2">
            No projects yet
          </h3>
          <p className="text-slate-500 mb-6">
            Get started by creating your first project
          </p>
          <Button asChild>
            <Link href="/projects/new">Create your first project</Link>
          </Button>
        </div>
      )}

      {/* Projects grid */}
      {!error && projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Link key={project.id} href={`/projects/${project.id}`}>
              <Card className="h-full transition-colors hover:bg-slate-800/50 hover:border-slate-700 cursor-pointer">
                <CardHeader>
                  <CardTitle className="text-lg text-slate-100">
                    {project.name}
                  </CardTitle>
                  <CardDescription className="flex gap-2 mt-2">
                    <TypeBadge type={project.type} />
                    <StatusBadge status={project.status} />
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-between text-sm text-slate-400">
                    <span>
                      {project.feature_count}{" "}
                      {project.feature_count === 1 ? "feature" : "features"}
                    </span>
                    <span>{formatDate(project.created_at)}</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
