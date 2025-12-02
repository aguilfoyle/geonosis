"""
Geonosis API - Main application entry point.

This module initializes the FastAPI application with:
- CORS middleware for frontend communication
- Database connection management
- Health check endpoints
- Lifespan events for startup/shutdown
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.database import init_db

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    
    On startup:
        - Logs application start
        - Tests database connection
    
    On shutdown:
        - Logs application shutdown
    """
    # Startup
    logger.info("Starting Geonosis API...")
    
    # Test database connection
    db_connected = await init_db()
    if not db_connected:
        logger.warning("Database connection failed - some features may be unavailable")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Geonosis API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered software development orchestration system",
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    """
    Root endpoint returning API information.
    
    Returns:
        dict: API name, status, version, and debug mode
    """
    return {
        "message": settings.app_name,
        "status": "operational",
        "version": "0.1.0",
        "debug": settings.debug,
    }


@app.get("/health")
async def health() -> dict:
    """
    Health check endpoint with detailed status.
    
    Checks database connectivity and returns overall health status.
    
    Returns:
        dict: Health status including database connection state
    """
    # Check database connection
    db_connected = await init_db()
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "database": "connected" if db_connected else "disconnected",
        "version": "0.1.0",
    }

