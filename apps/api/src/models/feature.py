"""
Feature model for Geonosis.

A Feature represents a distinct capability or user story within a Project.
Features are broken down into PBIs (Product Backlog Items) for implementation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, TimestampMixin, UUIDMixin
from src.models.enums import FeatureStatus

if TYPE_CHECKING:
    from src.models.pbi import PBI
    from src.models.project import Project


class Feature(UUIDMixin, TimestampMixin, Base):
    """
    A feature or user story within a project.

    Features represent distinct capabilities that need to be implemented.
    Each feature is broken down into one or more PBIs (Product Backlog Items)
    for backend and frontend implementation.

    Attributes:
        project_id: Reference to the parent project
        name: Short name for the feature
        description: Detailed description of the feature
        status: Current status in the feature lifecycle
        branch_name: Git branch name for this feature
        order: Display order within the project
        project: Parent project relationship
        pbis: List of PBIs implementing this feature
    """

    __tablename__ = "features"

    project_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[FeatureStatus] = mapped_column(
        Enum(FeatureStatus),
        default=FeatureStatus.PENDING,
        nullable=False,
    )
    branch_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="features",
    )
    pbis: Mapped[list["PBI"]] = relationship(
        "PBI",
        back_populates="feature",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Feature(id={self.id}, name='{self.name}', status={self.status.value})>"
