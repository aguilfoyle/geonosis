"""
Project model for Geonosis.

The Project is the top-level entity representing a software development
project being orchestrated by Geonosis agents.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, TimestampMixin, UUIDMixin
from src.models.enums import ProjectStatus, ProjectType

if TYPE_CHECKING:
    from src.models.agent_log import AgentLog
    from src.models.feature import Feature


class Project(UUIDMixin, TimestampMixin, Base):
    """
    A software development project being orchestrated by Geonosis.

    Projects contain features which are broken down into PBIs (Product Backlog Items)
    that are implemented by AI agents.

    Attributes:
        name: Human-readable project name
        epic: Full description of the project/feature/bug in markdown
        type: Whether this is a new project, bug fix, or feature addition
        status: Current status in the project lifecycle
        github_repo_url: URL to the GitHub repository (once created)
        github_repo_name: Name of the GitHub repository
        features: List of features belonging to this project
        logs: Agent activity logs for this project
    """

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    epic: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[ProjectType] = mapped_column(
        Enum(ProjectType),
        default=ProjectType.NEW_PROJECT,
        nullable=False,
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.DRAFT,
        nullable=False,
    )
    github_repo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_repo_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    features: Mapped[list["Feature"]] = relationship(
        "Feature",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    logs: Mapped[list["AgentLog"]] = relationship(
        "AgentLog",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def get_pr_url(self, pr_number: int) -> str | None:
        """
        Build the GitHub pull request URL for this project.

        Args:
            pr_number: The pull request number

        Returns:
            The full PR URL, or None if github_repo_url is not set
        """
        if not self.github_repo_url:
            return None
        # Remove trailing slash if present
        base_url = self.github_repo_url.rstrip("/")
        return f"{base_url}/pull/{pr_number}"

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status={self.status.value})>"
