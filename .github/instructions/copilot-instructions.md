# Geonosis Copilot Instructions

> **Last Updated:** 2025-12-03
> 
> **Maintainer Note:** Update this file when adding new conventions, patterns, or major architectural changes. Avoid listing specific files - focus on patterns.

## Project Overview

Geonosis is an AI-powered software development orchestration system that uses autonomous agents to build applications from requirements. Named after the Star Wars planet with droid factories.

Key concepts:
- **Projects**: Contain an epic (requirements) that get broken into features
- **Features**: Logical units of work, broken into PBIs
- **PBIs (Product Backlog Items)**: Atomic tasks assigned to backend or frontend agents
- **Agents**: AI agents (Manager, Backend Developer, Frontend Developer) that do the work

## Tech Stack

### Backend (apps/api/)
- **Runtime**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (use `Mapped[]` and `mapped_column()`)
- **Migrations**: Alembic
- **Validation**: Pydantic 2.x
- **Database**: PostgreSQL

### Frontend (apps/ui/)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict)
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: React Query for server state

### Infrastructure
- Docker & Docker Compose
- Turborepo monorepo
- Makefile for commands

## Project Structure (High-Level)

```
geonosis/
├── apps/
│   ├── api/src/           # FastAPI backend
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas  
│   │   ├── routers/       # API endpoints
│   │   └── services/      # Business logic
│   └── ui/src/            # Next.js frontend
│       ├── app/           # Pages (App Router)
│       └── components/    # React components
├── docs/agents/           # Agent rule files
└── .github/.prompts/      # Prompt templates
```

For detailed structure, explore the filesystem or see docs/.

## Code Patterns

### Backend: Creating an API Endpoint

Location: `apps/api/src/routers/{resource}.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter(prefix="/{resources}", tags=["{resources}"])

@router.get("/", response_model=list[{Resource}Response])
def list_{resources}(db: Session = Depends(get_db)):
    service = {Resource}Service(db)
    return service.list_all()

@router.post("/", response_model={Resource}Response, status_code=status.HTTP_201_CREATED)
def create_{resource}(data: {Resource}Create, db: Session = Depends(get_db)):
    service = {Resource}Service(db)
    return service.create(data)

@router.get("/{id}", response_model={Resource}Response)
def get_{resource}(id: UUID, db: Session = Depends(get_db)):
    service = {Resource}Service(db)
    result = service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="{Resource} not found")
    return result
```

### Backend: Creating a Model

Location: `apps/api/src/models/{resource}.py`

```python
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base, UUIDMixin, TimestampMixin

class {Resource}(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "{resources}"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # Add columns...
    
    # Foreign key with index
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("parents.id"), index=True)
    
    # Relationships
    parent: Mapped["Parent"] = relationship(back_populates="{resources}")
```

### Backend: Creating Schemas

Location: `apps/api/src/schemas/{resource}.py`

```python
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class {Resource}Base(BaseModel):
    name: str

class {Resource}Create({Resource}Base):
    pass

class {Resource}Response({Resource}Base):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime
```

### Frontend: Creating a Component

Location: `apps/ui/src/components/{feature}/{ComponentName}.tsx`

```typescript
// Server Component (default)
interface {ComponentName}Props {
  // props
}

export function {ComponentName}({ }: {ComponentName}Props) {
  return <div></div>;
}

// Client Component (only when needed)
"use client";
import { useState } from "react";
```

## ⚠️ Critical: Names to AVOID

### SQLAlchemy Reserved (NEVER use as column names)
- `metadata` → use `extra_data`
- `query` → use `query_string` or `search_query`
- `registry` → use `registry_name`

### Pydantic Reserved (NEVER use as field names)
- `model_config`
- `model_fields`
- `schema` → use `schema_name`

### Python Reserved
- `type` → use `type_` or `resource_type`
- `class` → use `class_` or `category`

## Database Enums

Defined in `src/models/enums.py`:

- **ProjectType**: NEW_PROJECT, EXISTING_PROJECT_BUG, EXISTING_PROJECT_FEATURE
- **ProjectStatus**: DRAFT → ANALYZING → FEATURES_PENDING_REVIEW → APPROVED → REPO_CREATING → REPO_CREATED → PBIS_CREATING → IN_PROGRESS → COMPLETED
- **FeatureStatus**: PENDING → IN_PROGRESS → PR_PENDING → COMPLETED
- **PBIType**: BACKEND, FRONTEND
- **PBIStatus**: PENDING → IN_PROGRESS → PR_CREATED → COMPLETED (with branches for PR_CHANGES_REQUESTED, BLOCKED, FAILED)
- **AgentMessageType**: THOUGHT, ACTION, CODE, ERROR, COMMUNICATION

## Git Conventions

### Branch Naming
- Feature: `feature/{short-description}` (e.g., `feature/user-authentication`)
- PBI: `{feature-short-desc}/{pbi-short-desc}` (e.g., `user-authentication/login-endpoint`)

### Commits
Use conventional commits:
- `feat: add user authentication endpoint`
- `fix: resolve database connection issue`
- `chore: update dependencies`
- `docs: add API documentation`

## Development Commands

```bash
make install          # Install all dependencies
make dev-api          # Start backend (localhost:8000)
make dev-ui           # Start frontend (localhost:3000)
make db-start         # Start PostgreSQL
make migrate          # Run migrations
make migrate-create name="description"  # Create migration
```

## Environment Variables

Required in `.env` (repo root):
```
DATABASE_URL=postgresql://geonosis:geonosis@localhost:5432/geonosis
GITHUB_TOKEN=ghp_...
GITHUB_USERNAME=...
ANTHROPIC_API_KEY=sk-ant-...  # Optional for now
```

## 🔄 Self-Maintenance

This file should stay current with the project. Copilot and developers share this responsibility.

### For Copilot

When you notice any of the following, proactively suggest an update to this file:

1. **New patterns**: If you help create a new code pattern not documented here, suggest adding it
2. **New conventions**: If a new naming convention or practice is established, flag it
3. **Contradictions**: If code contradicts these instructions, ask if instructions should be updated
4. **New reserved words**: If you encounter a new naming conflict, suggest adding it to the avoid list
5. **New enums/types**: If new enums are added to the codebase, suggest documenting them

When suggesting updates, output them in this format:

📝 **Suggested Update to copilot-instructions.md**

Section: [section name]
Change: [add/modify/remove]
Content:
```
[the content to add or change]
```
Reason: [why this update is needed]

### For Developers

Periodically (weekly or after major features), ask Copilot:

> "Review .github/copilot-instructions.md against the current codebase. Are there any patterns, conventions, or structures that are missing or outdated?"

### Update Checklist

When making significant changes, consider if these sections need updates:
- [ ] Tech Stack - new dependencies?
- [ ] Code Patterns - new patterns established?
- [ ] Names to Avoid - new conflicts discovered?
- [ ] Database Enums - new enums added?
- [ ] Development Commands - new make targets?
- [ ] Environment Variables - new env vars required?

### Version History

Track major updates here:

| Date | Change | Author |
|------|--------|--------|
| 2025-12-03 | Initial creation | Copilot |
