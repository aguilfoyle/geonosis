"use client";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ProjectType } from "@/types";

interface TypeBadgeProps {
  type: ProjectType;
  className?: string;
}

/**
 * Get the display label for a project type.
 */
function formatType(type: ProjectType): string {
  const typeLabels: Record<ProjectType, string> = {
    [ProjectType.NEW_PROJECT]: "New",
    [ProjectType.EXISTING_PROJECT_BUG]: "Bug Fix",
    [ProjectType.EXISTING_PROJECT_FEATURE]: "Feature",
  };

  return typeLabels[type] || type;
}

/**
 * Get the badge styling based on project type.
 */
function getTypeStyles(type: ProjectType): string {
  const styleMap: Record<ProjectType, string> = {
    [ProjectType.NEW_PROJECT]:
      "bg-primary/20 text-primary border-primary/30",
    [ProjectType.EXISTING_PROJECT_BUG]:
      "bg-red-500/20 text-red-300 border-red-500/30",
    [ProjectType.EXISTING_PROJECT_FEATURE]:
      "bg-blue-500/20 text-blue-300 border-blue-500/30",
  };

  return styleMap[type] || "";
}

/**
 * Type badge component for displaying project type.
 */
export function TypeBadge({ type, className }: TypeBadgeProps) {
  return (
    <Badge
      variant="outline"
      className={cn(getTypeStyles(type), className)}
    >
      {formatType(type)}
    </Badge>
  );
}
