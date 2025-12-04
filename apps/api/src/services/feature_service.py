"""
Feature service for business logic operations.

This service handles all CRUD operations and business logic
for Feature resources.
"""

from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from src.models import Feature, FeatureStatus, Project
from src.schemas.feature import FeatureCreate, FeatureUpdate


class FeatureService:
    """Service class for Feature operations."""

    def __init__(self, db: Session) -> None:
        """
        Initialize the service with a database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def list_by_project(self, project_id: UUID) -> list[Feature]:
        """
        Retrieve all features for a project.

        Args:
            project_id: UUID of the project

        Returns:
            List of features ordered by order field, then created_at
        """
        return (
            self.db.query(Feature)
            .options(joinedload(Feature.pbis))
            .filter(Feature.project_id == project_id)
            .order_by(Feature.order.asc(), Feature.created_at.asc())
            .all()
        )

    def get_by_id(self, feature_id: UUID) -> Feature | None:
        """
        Retrieve a feature by its ID.

        Args:
            feature_id: UUID of the feature to retrieve

        Returns:
            Feature if found, None otherwise
        """
        return (
            self.db.query(Feature)
            .options(joinedload(Feature.pbis))
            .filter(Feature.id == feature_id)
            .first()
        )

    def _get_next_order(self, project_id: UUID) -> int:
        """
        Get the next order value for a feature in a project.

        Args:
            project_id: UUID of the project

        Returns:
            Next order value (max + 1, or 0 if no features exist)
        """
        max_order = (
            self.db.query(func.max(Feature.order))
            .filter(Feature.project_id == project_id)
            .scalar()
        )
        return (max_order or -1) + 1

    def _verify_project_exists(self, project_id: UUID) -> Project:
        """
        Verify a project exists.

        Args:
            project_id: UUID of the project

        Returns:
            Project if found

        Raises:
            ValueError: If project not found
        """
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if project is None:
            raise ValueError(f"Project with id {project_id} not found")
        return project

    def create(self, data: FeatureCreate) -> Feature:
        """
        Create a new feature.

        Args:
            data: Feature creation data

        Returns:
            The newly created feature

        Raises:
            ValueError: If project not found
        """
        self._verify_project_exists(data.project_id)

        # Calculate order if not explicitly provided or is default
        order = data.order
        if order == 0:
            order = self._get_next_order(data.project_id)

        feature = Feature(
            name=data.name,
            description=data.description,
            project_id=data.project_id,
            status=FeatureStatus.PENDING,
            order=order,
        )
        self.db.add(feature)
        self.db.commit()
        self.db.refresh(feature)
        return feature

    def create_many(
        self, project_id: UUID, features: list[FeatureCreate]
    ) -> list[Feature]:
        """
        Bulk create features for a project.

        Useful for when Manager Agent generates multiple features at once.

        Args:
            project_id: UUID of the project
            features: List of feature creation data

        Returns:
            List of created features

        Raises:
            ValueError: If project not found
        """
        self._verify_project_exists(project_id)

        # Get starting order
        next_order = self._get_next_order(project_id)

        created_features: list[Feature] = []
        for i, data in enumerate(features):
            feature = Feature(
                name=data.name,
                description=data.description,
                project_id=project_id,
                status=FeatureStatus.PENDING,
                order=next_order + i,
            )
            self.db.add(feature)
            created_features.append(feature)

        self.db.commit()

        # Refresh all features to get generated fields
        for feature in created_features:
            self.db.refresh(feature)

        return created_features

    def update(self, feature_id: UUID, data: FeatureUpdate) -> Feature | None:
        """
        Update an existing feature.

        Args:
            feature_id: UUID of the feature to update
            data: Feature update data (only provided fields will be updated)

        Returns:
            Updated feature if found, None otherwise
        """
        feature = self.db.query(Feature).filter(Feature.id == feature_id).first()
        if feature is None:
            return None

        # Update only provided fields
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(feature, field, value)

        self.db.commit()
        self.db.refresh(feature)
        return feature

    def delete(self, feature_id: UUID) -> bool:
        """
        Delete a feature by ID.

        Args:
            feature_id: UUID of the feature to delete

        Returns:
            True if deleted, False if not found
        """
        feature = self.db.query(Feature).filter(Feature.id == feature_id).first()
        if feature is None:
            return False

        self.db.delete(feature)
        self.db.commit()
        return True

    def update_status(
        self, feature_id: UUID, status: FeatureStatus
    ) -> Feature | None:
        """
        Update only the status of a feature.

        Convenience method for status transitions.

        Args:
            feature_id: UUID of the feature
            status: New status value

        Returns:
            Updated feature if found, None otherwise
        """
        feature = self.db.query(Feature).filter(Feature.id == feature_id).first()
        if feature is None:
            return None

        feature.status = status
        self.db.commit()
        self.db.refresh(feature)
        return feature
