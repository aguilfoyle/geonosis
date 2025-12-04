"""
Pydantic schemas for Feature resources.

Features represent functional units of work within a Project.
Each Feature can contain multiple PBIs (Product Backlog Items).
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from src.models.enums import FeatureStatus


class FeatureBase(BaseModel):
    """Base schema with common Feature fields."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)


class FeatureCreate(FeatureBase):
    """Schema for creating a new Feature."""

    project_id: UUID
    order: int = Field(default=0, ge=0)


class FeatureUpdate(BaseModel):
    """
    Schema for updating an existing Feature.

    All fields are optional - only provided fields will be updated.
    """

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    status: FeatureStatus | None = None
    branch_name: str | None = None
    order: int | None = Field(default=None, ge=0)


class FeatureResponse(FeatureBase):
    """
    Full Feature response schema.

    Includes all fields returned when fetching a single Feature.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    status: FeatureStatus
    branch_name: str | None
    order: int
    created_at: datetime
    updated_at: datetime
    pbi_count: int = 0


class FeatureListResponse(BaseModel):
    """
    Summary Feature schema for listing.

    Used when listing Features within a Project.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: FeatureStatus
    branch_name: str | None
    order: int
    pbi_count: int = 0


class FeatureBulkCreateItem(BaseModel):
    """
    Single feature item for bulk creation.

    Used within FeatureBulkCreate for creating multiple features at once.
    """

    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    order: int | None = Field(default=None, ge=0)


class FeatureBulkCreate(BaseModel):
    """
    Request schema for bulk feature creation.

    Used by the Manager Agent to create all features for a project
    in a single request after analyzing the epic.
    """

    project_id: UUID
    features: list[FeatureBulkCreateItem] = Field(..., min_length=1)
