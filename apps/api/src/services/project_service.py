"""
Project service for business logic operations.

This service handles all CRUD operations and business logic
for Project resources.
"""

from uuid import UUID

from sqlalchemy.orm import Session, joinedload
from src.models import Project, ProjectStatus
from src.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service class for Project operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize the service with a database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def list_all(self) -> list[Project]:
        """
        Retrieve all projects ordered by creation date.

        Returns:
            List of all projects, newest first
        """
        return (
            self.db.query(Project)
            .order_by(Project.created_at.desc())
            .all()
        )

    def get_by_id(self, project_id: UUID) -> Project | None:
        """
        Retrieve a project by its ID.

        Args:
            project_id: UUID of the project to retrieve

        Returns:
            Project if found, None otherwise
        """
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, data: ProjectCreate) -> Project:
        """
        Create a new project.

        Args:
            data: Project creation data

        Returns:
            The newly created project
        """
        project = Project(
            name=data.name, # pyright: ignore[reportCallIssue] known SQLAlchemy + Pylance quirk. The code is correct and works.
            epic=data.epic, # pyright: ignore[reportCallIssue] known SQLAlchemy + Pylance quirk. The code is correct and works.
            type=data.type, # pyright: ignore[reportCallIssue] known SQLAlchemy + Pylance quirk. The code is correct and works.
            status=ProjectStatus.DRAFT, # pyright: ignore[reportCallIssue] known SQLAlchemy + Pylance quirk. The code is correct and works.
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project_id: UUID, data: ProjectUpdate) -> Project | None:
        """
        Update an existing project.

        Args:
            project_id: UUID of the project to update
            data: Project update data (only provided fields will be updated)

        Returns:
            Updated project if found, None otherwise
        """
        project = self.get_by_id(project_id)
        if project is None:
            return None

        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: UUID) -> bool:
        """
        Delete a project by ID.

        Args:
            project_id: UUID of the project to delete

        Returns:
            True if deleted, False if not found
        """
        project = self.get_by_id(project_id)
        if project is None:
            return False

        self.db.delete(project)
        self.db.commit()
        return True

    def get_with_features(self, project_id: UUID) -> Project | None:
        """
        Retrieve a project with its features eagerly loaded.

        Args:
            project_id: UUID of the project to retrieve

        Returns:
            Project with features loaded if found, None otherwise
        """
        return (
            self.db.query(Project)
            .options(joinedload(Project.features))
            .filter(Project.id == project_id)
            .first()
        )
