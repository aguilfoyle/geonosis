"""
Pydantic schemas for Project resource.

These schemas handle request validation and response serialization
for the Project API endpoints.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from src.models.enums import ProjectStatus, ProjectType


class ProjectBase(BaseModel):
    """Base schema with common project fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    epic: str = Field(..., min_length=1, description="Project requirements in markdown")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    type: ProjectType = Field(
        default=ProjectType.NEW_PROJECT,
        description="Type of project being created",
    )


class ProjectUpdate(BaseModel):
    """Schema for updating a project. All fields are optional."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated project name",
    )
    epic: str | None = Field(None, description="Updated project requirements")
    status: ProjectStatus | None = Field(None, description="Updated project status")


class ProjectResponse(ProjectBase):
    """Schema for full project response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    type: ProjectType
    status: ProjectStatus
    github_repo_url: str | None
    github_repo_name: str | None
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    """Schema for project list item with summary info."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    type: ProjectType
    status: ProjectStatus
    created_at: datetime
    feature_count: int = Field(default=0, description="Number of features in project")
