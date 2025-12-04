/**
 * API client service for the Geonosis backend.
 */

import type {
    Project,
    ProjectCreate,
    ProjectListItem,
    ProjectUpdate,
} from "@/types";

// =============================================================================
// Configuration
// =============================================================================

/**
 * Get the API base URL based on environment (server vs client).
 * - Server-side: Use API_URL_INTERNAL for container-to-container communication
 * - Client-side: Use NEXT_PUBLIC_API_URL for browser requests
 */
function getBaseUrl(): string {
  if (typeof window === "undefined") {
    // Server-side: prefer internal URL for container communication
    return (
      process.env.API_URL_INTERNAL ||
      process.env.NEXT_PUBLIC_API_URL ||
      "http://localhost:8000"
    );
  }
  // Client-side: use public URL
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

const API_PATH = "/api/v1";

// =============================================================================
// Fetch Wrapper
// =============================================================================

interface ApiError {
  detail: string;
}

interface FetchOptions extends RequestInit {
  /**
   * Next.js specific caching options
   */
  next?: {
    revalidate?: number | false;
    tags?: string[];
  };
}

async function apiFetch<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const url = `${getBaseUrl()}${API_PATH}${endpoint}`;

  const headers: HeadersInit = {
    ...options.headers,
  };

  // Add Content-Type for requests with body
  if (options.body) {
    (headers as Record<string, string>)["Content-Type"] = "application/json";
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // Handle no-content responses (e.g., DELETE)
  if (response.status === 204) {
    return undefined as T;
  }

  const data = await response.json();

  if (!response.ok) {
    const error = data as ApiError;
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return data as T;
}

// =============================================================================
// Projects API
// =============================================================================

export const projectsApi = {
  /**
   * List all projects.
   */
  async list(): Promise<ProjectListItem[]> {
    return apiFetch<ProjectListItem[]>("/projects/", {
      cache: "no-store",
    });
  },

  /**
   * Get a project by ID.
   */
  async get(id: string): Promise<Project> {
    return apiFetch<Project>(`/projects/${id}`, {
      cache: "no-store",
    });
  },

  /**
   * Create a new project.
   */
  async create(data: ProjectCreate): Promise<Project> {
    return apiFetch<Project>("/projects/", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing project.
   */
  async update(id: string, data: ProjectUpdate): Promise<Project> {
    return apiFetch<Project>(`/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  /**
   * Delete a project.
   */
  async delete(id: string): Promise<void> {
    return apiFetch<void>(`/projects/${id}`, {
      method: "DELETE",
    });
  },
};
