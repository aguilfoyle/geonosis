import { PageContainer } from "@/components/layout";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function ProjectsLoading() {
  return (
    <PageContainer
      title="Projects"
      description="Manage your AI-powered development projects"
    >
      {/* Header with Create button placeholder */}
      <div className="flex justify-between items-center mb-8">
        <div />
        <Skeleton className="h-10 w-32" />
      </div>

      {/* Skeleton grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <Card key={i} className="h-full">
            <CardHeader>
              {/* Title skeleton */}
              <Skeleton className="h-6 w-3/4 mb-2" />
              {/* Badges skeleton */}
              <div className="flex gap-2 mt-2">
                <Skeleton className="h-5 w-16 rounded-md" />
                <Skeleton className="h-5 w-20 rounded-md" />
              </div>
            </CardHeader>
            <CardContent>
              {/* Meta info skeleton */}
              <div className="flex justify-between">
                <Skeleton className="h-4 w-20" />
                <Skeleton className="h-4 w-24" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </PageContainer>
  );
}
