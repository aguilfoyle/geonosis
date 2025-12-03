"""
PBI (Product Backlog Item) model for Geonosis.

A PBI represents a single unit of work within a Feature, typically
either a backend or frontend task that an AI agent will implement.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, TimestampMixin, UUIDMixin
from src.models.enums import PBIStatus, PBIType, PRStatus

if TYPE_CHECKING:
    from src.models.feature import Feature


class PBI(UUIDMixin, TimestampMixin, Base):
    """
    A Product Backlog Item representing a unit of work.

    PBIs are the atomic units of work that AI agents implement.
    Each PBI is either a backend or frontend task and can have
    dependencies on other PBIs.

    Attributes:
        feature_id: Reference to the parent feature
        title: Short title for the PBI
        description: Detailed description of the work
        type: BACKEND or FRONTEND
        status: Current status in the PBI lifecycle
        assigned_agent: Name of the agent assigned to this PBI
        branch_name: Git branch name for this PBI
        pr_number: GitHub pull request number
        pr_status: Status of the pull request
        blocked_by_id: ID of the PBI this one depends on
        order: Display/execution order within the feature
        feature: Parent feature relationship
        blocked_by: PBI that blocks this one
        blocking: PBIs that this one blocks
    """

    __tablename__ = "pbis"

    feature_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("features.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[PBIType] = mapped_column(
        Enum(PBIType),
        nullable=False,
    )
    status: Mapped[PBIStatus] = mapped_column(
        Enum(PBIStatus),
        default=PBIStatus.PENDING,
        nullable=False,
    )
    assigned_agent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    branch_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pr_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pr_status: Mapped[PRStatus | None] = mapped_column(
        Enum(PRStatus),
        nullable=True,
    )
    blocked_by_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pbis.id"),
        nullable=True,
    )
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    feature: Mapped["Feature"] = relationship(
        "Feature",
        back_populates="pbis",
    )

    # Self-referential relationship for dependencies
    blocked_by: Mapped["PBI | None"] = relationship(
        "PBI",
        remote_side="PBI.id",
        foreign_keys=[blocked_by_id],
        back_populates="blocking",
    )
    blocking: Mapped[list["PBI"]] = relationship(
        "PBI",
        foreign_keys=[blocked_by_id],
        back_populates="blocked_by",
    )

    def get_pr_url(self, github_repo_url: str) -> str | None:
        """
        Build the GitHub pull request URL for this PBI.

        Args:
            github_repo_url: The base GitHub repository URL

        Returns:
            The full PR URL, or None if pr_number is not set
        """
        if not self.pr_number or not github_repo_url:
            return None
        # Remove trailing slash if present
        base_url = github_repo_url.rstrip("/")
        return f"{base_url}/pull/{self.pr_number}"

    def __repr__(self) -> str:
        return f"<PBI(id={self.id}, title='{self.title}', type={self.type.value}, status={self.status.value})>"
