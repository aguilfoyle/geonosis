"""
Enum definitions for Geonosis database models.

This module defines all enumeration types used throughout the application
for type-safe status tracking and categorization.
"""

from enum import Enum


class ProjectType(str, Enum):
    """
    Type of project being created or modified.
    
    - NEW_PROJECT: Creating a brand new project from scratch
    - EXISTING_PROJECT_BUG: Fixing a bug in an existing project
    - EXISTING_PROJECT_FEATURE: Adding a feature to an existing project
    """

    NEW_PROJECT = "NEW_PROJECT"
    EXISTING_PROJECT_BUG = "EXISTING_PROJECT_BUG"
    EXISTING_PROJECT_FEATURE = "EXISTING_PROJECT_FEATURE"


class ProjectStatus(str, Enum):
    """
    Status of a project through its lifecycle.
    
    Tracks the project from initial draft through analysis,
    feature approval, repository creation, and completion.
    """

    DRAFT = "DRAFT"
    ANALYZING = "ANALYZING"
    FEATURES_PENDING_REVIEW = "FEATURES_PENDING_REVIEW"
    FEATURES_REJECTED = "FEATURES_REJECTED"
    APPROVED = "APPROVED"
    REPO_CREATING = "REPO_CREATING"
    REPO_CREATED = "REPO_CREATED"
    PBIS_CREATING = "PBIS_CREATING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class FeatureStatus(str, Enum):
    """
    Status of a feature within a project.
    
    Tracks individual features from pending through completion.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    PR_PENDING = "PR_PENDING"
    COMPLETED = "COMPLETED"


class PBIType(str, Enum):
    """
    Type of Product Backlog Item.
    
    - BACKEND: Server-side implementation work
    - FRONTEND: Client-side implementation work
    """

    BACKEND = "BACKEND"
    FRONTEND = "FRONTEND"


class PBIStatus(str, Enum):
    """
    Status of a Product Backlog Item through its lifecycle.
    
    Tracks PBIs from pending through PR creation, review, and completion.
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    PR_CREATED = "PR_CREATED"
    PR_CHANGES_REQUESTED = "PR_CHANGES_REQUESTED"
    PR_APPROVED = "PR_APPROVED"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class PRStatus(str, Enum):
    """
    Status of a Pull Request.
    
    Tracks PRs from open through review and merge/close.
    """

    OPEN = "OPEN"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    APPROVED = "APPROVED"
    MERGED = "MERGED"
    CLOSED = "CLOSED"


class AgentMessageType(str, Enum):
    """
    Type of message from an AI agent.
    
    - THOUGHT: Internal reasoning or planning
    - ACTION: Description of an action being taken
    - CODE: Code being generated or modified
    - ERROR: Error messages or failures
    - COMMUNICATION: Messages to users or other agents
    """

    THOUGHT = "THOUGHT"
    ACTION = "ACTION"
    CODE = "CODE"
    ERROR = "ERROR"
    COMMUNICATION = "COMMUNICATION"
