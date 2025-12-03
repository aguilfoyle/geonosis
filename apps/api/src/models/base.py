"""
Base model mixins for Geonosis database models.

This module provides reusable mixins that add common fields to SQLAlchemy models:
- TimestampMixin: Adds created_at and updated_at timestamps
- UUIDMixin: Adds a UUID primary key

Usage:
    from src.models.base import Base, UUIDMixin, TimestampMixin

    class Project(UUIDMixin, TimestampMixin, Base):
        __tablename__ = "projects"
        name: Mapped[str] = mapped_column(String(255))
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamp columns.

    - created_at: Set automatically when the record is created
    - updated_at: Updated automatically on every modification

    Both timestamps are stored in UTC.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class UUIDMixin:
    """
    Mixin that adds a UUID primary key column.

    The id is automatically generated using uuid4 when a new record is created.
    Uses PostgreSQL's native UUID type for efficient storage.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


__all__ = ["Base", "TimestampMixin", "UUIDMixin"]
