"""
AgentLog model for Geonosis.

AgentLog records the activity of AI agents working on projects and PBIs,
providing an audit trail and debugging information.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, TimestampMixin, UUIDMixin
from src.models.enums import AgentMessageType

if TYPE_CHECKING:
    from src.models.pbi import PBI
    from src.models.project import Project


class AgentLog(UUIDMixin, TimestampMixin, Base):
    """
    A log entry from an AI agent.

    AgentLogs capture the thoughts, actions, and outputs of AI agents
    as they work on projects and PBIs. This provides transparency
    into the agent's decision-making process.

    Attributes:
        project_id: Reference to the project this log belongs to
        pbi_id: Optional reference to a specific PBI
        agent_name: Name of the agent that created this log
        message_type: Type of message (THOUGHT, ACTION, CODE, ERROR, COMMUNICATION)
        content: The actual log message content
        extra_data: Additional structured data as JSON
        project: Parent project relationship
        pbi: Optional PBI relationship
    """

    __tablename__ = "agent_logs"

    project_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )
    pbi_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("pbis.id"),
        nullable=True,
        index=True,
    )
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    message_type: Mapped[AgentMessageType] = mapped_column(
        Enum(AgentMessageType),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    extra_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="logs",
    )
    pbi: Mapped["PBI | None"] = relationship(
        "PBI",
    )

    def __repr__(self) -> str:
        return f"<AgentLog(id={self.id}, agent='{self.agent_name}', type={self.message_type.value})>"
