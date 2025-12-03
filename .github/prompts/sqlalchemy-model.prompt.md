# Create SQLAlchemy Model

Create a new SQLAlchemy model in apps/api/src/models/

## Requirements

- Model name: {ModelName}
- Table name: {table_name}
- Fields: {list fields}

## Template

Follow this structure:
```python
from __future__ import annotations
from sqlalchemy import String, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from src.models.base import Base, UUIDMixin, TimestampMixin
from src.models.enums import {EnumName}


class {ModelName}(UUIDMixin, TimestampMixin, Base):
    """
    {Description}
    """
    __tablename__ = "{table_name}"

    # Columns
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Foreign Keys
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("parents.id"), nullable=False, index=True)
    
    # Relationships
    parent: Mapped["Parent"] = relationship(back_populates="{table_name}")

    def __repr__(self) -> str:
        return f"<{ModelName}(id={self.id}, name='{self.name}')>"
```

## Watch Out For
- NEVER use reserved names: metadata, query, registry
- Use Mapped[] and mapped_column() (SQLAlchemy 2.0 style)
- Add index=True on foreign keys
- Use proper relationship back_populates
- Add __repr__ for debugging
- Export in models/__init__.py
