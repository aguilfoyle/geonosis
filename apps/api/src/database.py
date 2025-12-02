"""
Database connection and session management for Geonosis API.

This module provides:
- SQLAlchemy engine configuration
- Session factory for database operations
- Base class for ORM models
- Dependency injection for FastAPI routes
- Database initialization and health checks

Usage:
    from src.database import get_db, Base
    
    # In FastAPI routes
    @app.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
    
    # For models
    class Item(Base):
        __tablename__ = "items"
        id = Column(Integer, primary_key=True)
"""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from src.config import get_settings

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create SQLAlchemy engine
# pool_pre_ping ensures connections are valid before use
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.debug,
)

# Session factory
# autocommit=False: explicit commits required
# autoflush=False: explicit flushes required for better control
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    
    Yields a SQLAlchemy session and ensures it is closed after use.
    Use with FastAPI's Depends() for automatic session management.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db() -> bool:
    """
    Initialize and test the database connection.
    
    Attempts to connect to the database and execute a simple query
    to verify connectivity. Logs the result.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Test the connection with a simple query
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        
        logger.info("Database connection established successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return False
