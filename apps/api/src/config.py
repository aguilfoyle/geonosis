"""
Configuration management for Geonosis API.

This module uses pydantic-settings to manage configuration from environment
variables and .env files. Settings are loaded once and cached for performance.

Environment variables can be set with or without the GEONOSIS_ prefix:
    - DATABASE_URL or GEONOSIS_DATABASE_URL
    - GITHUB_TOKEN or GEONOSIS_GITHUB_TOKEN
    - etc.

Usage:
    from src.config import get_settings
    
    settings = get_settings()
    print(settings.database_url)
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Calculate the repository root path
# config.py -> src -> api -> apps -> root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = REPO_ROOT / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables.
    The .env file in the repository root is automatically loaded.
    """
    
    # Application
    app_name: str = "Geonosis API"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str = Field(..., description="PostgreSQL connection string")
    
    # GitHub Integration
    github_token: str | None = Field(
        default=None,
        description="GitHub Personal Access Token with repo scope"
    )
    github_username: str | None = Field(
        default=None,
        description="GitHub username for API operations"
    )
    
    # Anthropic Claude
    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key for Claude"
    )
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class SettingsWithPrefix(Settings):
    """Settings class that reads GEONOSIS_ prefixed environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        env_prefix="GEONOSIS_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Settings are loaded from environment variables and .env file.
    The function is cached so settings are only loaded once.
    
    First attempts to load with GEONOSIS_ prefix, falls back to no prefix.
    
    Returns:
        Settings: Application configuration instance
    """
    # Try loading with prefix first, fall back to no prefix
    try:
        return SettingsWithPrefix()
    except Exception:
        return Settings()
