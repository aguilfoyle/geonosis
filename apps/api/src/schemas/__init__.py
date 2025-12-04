# Pydantic schemas for request/response
"""
Pydantic schemas for Geonosis API.

All request and response schemas should be defined in this package
and imported here for easy access.
"""

from src.schemas.feature import (FeatureBase, FeatureBulkCreate,
                                 FeatureBulkCreateItem, FeatureCreate,
                                 FeatureListResponse, FeatureResponse,
                                 FeatureUpdate)
from src.schemas.project import (ProjectBase, ProjectCreate,
                                 ProjectListResponse, ProjectResponse,
                                 ProjectUpdate)

__all__: list[str] = [
    # Feature schemas
    "FeatureBase",
    "FeatureBulkCreate",
    "FeatureBulkCreateItem",
    "FeatureCreate",
    "FeatureListResponse",
    "FeatureResponse",
    "FeatureUpdate",
    # Project schemas
    "ProjectBase",
    "ProjectCreate",
    "ProjectListResponse",
    "ProjectResponse",
    "ProjectUpdate",
]
