"""
Projects API router.

Handles all CRUD operations for Project resources.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.project import (ProjectCreate, ProjectListResponse,
                                 ProjectResponse, ProjectUpdate)
from src.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectListResponse])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectListResponse]:
    """
    List all projects.

    Returns a list of all projects with summary information,
    ordered by creation date (newest first).
    """
    service = ProjectService(db)
    projects = service.list_all()

    # Compute feature_count for each project
    return [
        ProjectListResponse(
            id=project.id,
            name=project.name,
            type=project.type,
            status=project.status,
            created_at=project.created_at,
            feature_count=len(project.features),
        )
        for project in projects
    ]


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """
    Create a new project.

    Creates a project with DRAFT status. The epic field should contain
    the project requirements in markdown format.
    """
    service = ProjectService(db)
    return service.create(data)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """
    Get a project by ID.

    Returns the full project details including GitHub repository info.
    """
    service = ProjectService(db)
    project = service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    """
    Update a project.

    Only provided fields will be updated. Use this to change
    project name, epic, or status.
    """
    service = ProjectService(db)
    project = service.update(project_id, data)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """
    Delete a project.

    This will also delete all associated features, PBIs, and logs
    due to cascade delete.
    """
    service = ProjectService(db)
    deleted = service.delete(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return {"message": "Project deleted"}
