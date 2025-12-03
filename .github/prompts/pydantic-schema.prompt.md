# Create Pydantic Schema

Create Pydantic schemas in apps/api/src/schemas/

## Requirements

- Schema name: {SchemaName}
- Purpose: {Create/Update/Response}
- Fields: {list fields}

## Template

Follow this structure:
```python
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from src.models.enums import {EnumName}


class {SchemaName}Base(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class {SchemaName}Create({SchemaName}Base):
    """Schema for creating a new {entity}"""
    pass


class {SchemaName}Update(BaseModel):
    """Schema for updating a {entity} (all fields optional)"""
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class {SchemaName}Response({SchemaName}Base):
    """Schema for {entity} responses"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: {EnumName}
    created_at: datetime
    updated_at: datetime
```

## Watch Out For
- NEVER use reserved names: model_config, model_fields, schema
- Use ConfigDict(from_attributes=True) for ORM compatibility
- Use Field() for validation constraints
- Make Update schemas have all optional fields
- Export in schemas/__init__.py
