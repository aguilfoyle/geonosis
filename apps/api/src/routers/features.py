"""
Features API router.

Handles all CRUD operations for Feature resources.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.feature import (FeatureBulkCreate, FeatureCreate,
                                 FeatureListResponse, FeatureResponse,
                                 FeatureUpdate)
from src.services.feature_service import FeatureService

router = APIRouter(prefix="/features", tags=["features"])


# =============================================================================
# Endpoints
# =============================================================================


@router.get("/project/{project_id}", response_model=list[FeatureListResponse])
def list_features_by_project(
    project_id: UUID,
    db: Session = Depends(get_db),
) -> list[FeatureListResponse]:
    """
    List all features for a project.

    Returns features ordered by their order field, then by creation date.
    Each feature includes a count of its PBIs.
    """
    service = FeatureService(db)
    features = service.list_by_project(project_id)

    return [
        FeatureListResponse(
            id=feature.id,
            name=feature.name,
            status=feature.status,
            branch_name=feature.branch_name,
            order=feature.order,
            pbi_count=len(feature.pbis),
        )
        for feature in features
    ]


@router.post(
    "/",
    response_model=FeatureResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feature(
    data: FeatureCreate,
    db: Session = Depends(get_db),
) -> FeatureResponse:
    """
    Create a new feature.

    The feature will be created with PENDING status.
    If order is not provided, it will be set to the next available order
    for the project.
    """
    service = FeatureService(db)

    try:
        feature = service.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return FeatureResponse(
        id=feature.id,
        name=feature.name,
        description=feature.description,
        project_id=feature.project_id,
        status=feature.status,
        branch_name=feature.branch_name,
        order=feature.order,
        created_at=feature.created_at,
        updated_at=feature.updated_at,
        pbi_count=len(feature.pbis) if feature.pbis else 0,
    )


@router.post(
    "/bulk",
    response_model=list[FeatureResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_features_bulk(
    data: FeatureBulkCreate,
    db: Session = Depends(get_db),
) -> list[FeatureResponse]:
    """
    Create multiple features at once.

    This endpoint is designed for the Manager Agent to create
    all features for a project in a single request.
    Features will be assigned sequential order values.
    """
    service = FeatureService(db)

    # Convert bulk items to FeatureCreate objects
    feature_creates = [
        FeatureCreate(
            project_id=data.project_id,
            name=item.name,
            description=item.description,
            order=item.order if item.order is not None else 0,
        )
        for item in data.features
    ]

    try:
        features = service.create_many(data.project_id, feature_creates)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return [
        FeatureResponse(
            id=feature.id,
            name=feature.name,
            description=feature.description,
            project_id=feature.project_id,
            status=feature.status,
            branch_name=feature.branch_name,
            order=feature.order,
            created_at=feature.created_at,
            updated_at=feature.updated_at,
            pbi_count=0,
        )
        for feature in features
    ]


@router.get("/{feature_id}", response_model=FeatureResponse)
def get_feature(
    feature_id: UUID,
    db: Session = Depends(get_db),
) -> FeatureResponse:
    """
    Get a feature by ID.

    Returns the full feature details including PBI count.
    """
    service = FeatureService(db)
    feature = service.get_by_id(feature_id)

    if feature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found",
        )

    return FeatureResponse(
        id=feature.id,
        name=feature.name,
        description=feature.description,
        project_id=feature.project_id,
        status=feature.status,
        branch_name=feature.branch_name,
        order=feature.order,
        created_at=feature.created_at,
        updated_at=feature.updated_at,
        pbi_count=len(feature.pbis) if feature.pbis else 0,
    )


@router.patch("/{feature_id}", response_model=FeatureResponse)
def update_feature(
    feature_id: UUID,
    data: FeatureUpdate,
    db: Session = Depends(get_db),
) -> FeatureResponse:
    """
    Update a feature.

    Only provided fields will be updated.
    """
    service = FeatureService(db)
    feature = service.update(feature_id, data)

    if feature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found",
        )

    # Re-fetch to get pbis loaded
    feature = service.get_by_id(feature_id)

    if feature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found",
        )

    return FeatureResponse(
        id=feature.id,
        name=feature.name,
        description=feature.description,
        project_id=feature.project_id,
        status=feature.status,
        branch_name=feature.branch_name,
        order=feature.order,
        created_at=feature.created_at,
        updated_at=feature.updated_at,
        pbi_count=len(feature.pbis) if feature.pbis else 0,
    )


@router.delete("/{feature_id}")
def delete_feature(
    feature_id: UUID,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Delete a feature.

    This will also delete all associated PBIs due to cascade delete.
    """
    service = FeatureService(db)
    deleted = service.delete(feature_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found",
        )

    return {"message": "Feature deleted"}
