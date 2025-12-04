"use client";

import { PageContainer } from "@/components/layout";
import { Button } from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
import { projectsApi } from "@/services/api";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function NewProjectPage() {
  const router = useRouter();
  const { toast } = useToast();

  const [name, setName] = useState("");
  const [epic, setEpic] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous error
    setError(null);

    // Validate
    if (!name.trim()) {
      setError("Project name is required");
      return;
    }
    if (!epic.trim()) {
      setError("Epic / Requirements is required");
      return;
    }

    setIsSubmitting(true);

    try {
      const project = await projectsApi.create({
        name: name.trim(),
        epic: epic.trim(),
      });
      toast({
        title: "Project created",
        description: "Your project has been created successfully.",
      });
      router.push(`/projects/${project.id}`);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create project";
      setError(message);
      toast({
        title: "Error",
        description: message,
        variant: "destructive",
      });
      setIsSubmitting(false);
    }
  };

  const clearError = () => {
    if (error) setError(null);
  };

  return (
    <PageContainer title="Create New Project">
      <Card className="max-w-2xl">
        <form onSubmit={handleSubmit}>
          <CardHeader>
            <CardTitle>Project Details</CardTitle>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Error display */}
            {error && (
              <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300 text-sm">
                {error}
              </div>
            )}

            {/* Project Name */}
            <div className="space-y-2">
              <Label htmlFor="name">Project Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="My Awesome Project"
                value={name}
                onChange={(e) => {
                  setName(e.target.value);
                  clearError();
                }}
                disabled={isSubmitting}
                required
              />
            </div>

            {/* Epic / Requirements */}
            <div className="space-y-2">
              <Label htmlFor="epic">Epic / Requirements</Label>
              <Textarea
                id="epic"
                placeholder="Describe what you want to build..."
                value={epic}
                onChange={(e) => {
                  setEpic(e.target.value);
                  clearError();
                }}
                disabled={isSubmitting}
                rows={10}
                required
              />
              <p className="text-xs text-slate-500">
                Write your requirements in markdown format. Be as detailed as
                possible to get the best results.
              </p>
            </div>
          </CardContent>

          <CardFooter className="flex justify-between">
            <Button asChild variant="ghost" disabled={isSubmitting}>
              <Link href="/projects">Cancel</Link>
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Project"}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </PageContainer>
  );
}
