# API route handlers
"""
API routers for Geonosis API.

All FastAPI routers should be defined in this package
and imported here for easy registration with the app.
"""

from src.routers.features import router as features_router
from src.routers.projects import router as projects_router

__all__: list[str] = ["features_router", "projects_router"]
