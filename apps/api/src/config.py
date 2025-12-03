"""
Configuration management for Geonosis API.

This module uses pydantic-settings to manage configuration from environment
variables and .env files. Settings are loaded once and cached for performance.

Usage:
    from src.config import get_settings
    
    settings = get_settings()
    print(settings.database_url)
"""

from functools import lru_cache
from pathlib import Path

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
    
    # Database (required - will fail fast if not set)
    database_url: str
    
    # GitHub Integration
    github_token: str | None = None
    github_username: str | None = None
    
    # Anthropic Claude
    anthropic_api_key: str | None = None
    
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


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Settings are loaded from environment variables and .env file.
    The function is cached so settings are only loaded once.
    
    Returns:
        Settings: Application configuration instance
    """
    return Settings()
