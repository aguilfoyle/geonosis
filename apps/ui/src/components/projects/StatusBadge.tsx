"use client";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ProjectStatus } from "@/types";

interface StatusBadgeProps {
  status: ProjectStatus;
  className?: string;
}

/**
 * Format status text from SNAKE_CASE to readable format.
 * e.g., "FEATURES_PENDING_REVIEW" → "Pending Review"
 */
function formatStatus(status: ProjectStatus): string {
  const statusLabels: Record<ProjectStatus, string> = {
    [ProjectStatus.DRAFT]: "Draft",
    [ProjectStatus.ANALYZING]: "Analyzing",
    [ProjectStatus.FEATURES_PENDING_REVIEW]: "Pending Review",
    [ProjectStatus.FEATURES_REJECTED]: "Rejected",
    [ProjectStatus.APPROVED]: "Approved",
    [ProjectStatus.REPO_CREATING]: "Creating Repo",
    [ProjectStatus.REPO_CREATED]: "Repo Created",
    [ProjectStatus.PBIS_CREATING]: "Creating PBIs",
    [ProjectStatus.IN_PROGRESS]: "In Progress",
    [ProjectStatus.COMPLETED]: "Completed",
    [ProjectStatus.FAILED]: "Failed",
  };

  return statusLabels[status] || status;
}

/**
 * Get the badge styling based on status.
 */
function getStatusStyles(status: ProjectStatus): string {
  const styleMap: Record<ProjectStatus, string> = {
    [ProjectStatus.DRAFT]:
      "bg-slate-500/20 text-slate-300 border-slate-500/30",
    [ProjectStatus.ANALYZING]:
      "bg-blue-500/20 text-blue-300 border-blue-500/30",
    [ProjectStatus.FEATURES_PENDING_REVIEW]:
      "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
    [ProjectStatus.FEATURES_REJECTED]:
      "bg-red-500/20 text-red-300 border-red-500/30",
    [ProjectStatus.APPROVED]:
      "bg-green-500/20 text-green-300 border-green-500/30",
    [ProjectStatus.REPO_CREATING]:
      "bg-blue-500/20 text-blue-300 border-blue-500/30",
    [ProjectStatus.REPO_CREATED]:
      "bg-blue-500/20 text-blue-300 border-blue-500/30",
    [ProjectStatus.PBIS_CREATING]:
      "bg-blue-500/20 text-blue-300 border-blue-500/30",
    [ProjectStatus.IN_PROGRESS]:
      "bg-purple-500/20 text-purple-300 border-purple-500/30",
    [ProjectStatus.COMPLETED]:
      "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    [ProjectStatus.FAILED]:
      "bg-red-500/20 text-red-300 border-red-500/30",
  };

  return styleMap[status] || "";
}

/**
 * Status badge component for displaying project status.
 */
export function StatusBadge({ status, className }: StatusBadgeProps) {
  return (
    <Badge
      variant="outline"
      className={cn(getStatusStyles(status), className)}
    >
      {formatStatus(status)}
    </Badge>
  );
}
