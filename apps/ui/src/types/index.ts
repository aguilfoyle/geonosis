/**
 * TypeScript type definitions for the Geonosis API.
 *
 * These types mirror the backend Pydantic schemas.
 */

// =============================================================================
// Enums (as const objects for better TypeScript ergonomics)
// =============================================================================

export const ProjectType = {
  NEW_PROJECT: "NEW_PROJECT",
  EXISTING_PROJECT_BUG: "EXISTING_PROJECT_BUG",
  EXISTING_PROJECT_FEATURE: "EXISTING_PROJECT_FEATURE",
} as const;

export type ProjectType = (typeof ProjectType)[keyof typeof ProjectType];

export const ProjectStatus = {
  DRAFT: "DRAFT",
  ANALYZING: "ANALYZING",
  FEATURES_PENDING_REVIEW: "FEATURES_PENDING_REVIEW",
  FEATURES_REJECTED: "FEATURES_REJECTED",
  APPROVED: "APPROVED",
  REPO_CREATING: "REPO_CREATING",
  REPO_CREATED: "REPO_CREATED",
  PBIS_CREATING: "PBIS_CREATING",
  IN_PROGRESS: "IN_PROGRESS",
  COMPLETED: "COMPLETED",
  FAILED: "FAILED",
} as const;

export type ProjectStatus = (typeof ProjectStatus)[keyof typeof ProjectStatus];

// =============================================================================
// Project Interfaces
// =============================================================================

/**
 * Full project response from the API.
 */
export interface Project {
  id: string;
  name: string;
  epic: string;
  type: ProjectType;
  status: ProjectStatus;
  github_repo_url: string | null;
  github_repo_name: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Project list item (summary) from the API.
 */
export interface ProjectListItem {
  id: string;
  name: string;
  type: ProjectType;
  status: ProjectStatus;
  created_at: string;
  feature_count: number;
}

/**
 * Payload for creating a new project.
 */
export interface ProjectCreate {
  name: string;
  epic: string;
  type?: ProjectType;
}

/**
 * Payload for updating an existing project.
 */
export interface ProjectUpdate {
  name?: string;
  epic?: string;
  status?: ProjectStatus;
}
