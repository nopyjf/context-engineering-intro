"""
Configuration management using pydantic-settings.

This module handles all application configuration including:
- LLM provider settings
- Brave Search API configuration
- Gmail OAuth2 configuration
- Application environment settings
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be configured via environment variables or .env file.
    API keys must be provided and cannot be empty.
    """

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(
        default="openai",
        description="LLM provider (openai, anthropic, gemini)"
    )
    llm_api_key: str = Field(
        ...,
        description="API key for the LLM provider"
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Model name to use"
    )
    llm_base_url: Optional[str] = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API"
    )

    # Brave Search Configuration
    brave_api_key: str = Field(
        ...,
        description="Brave Search API key (get from https://brave.com/search/api/)"
    )
    brave_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/web/search",
        description="Brave Search API endpoint"
    )

    # Gmail OAuth2 Configuration
    gmail_credentials_path: str = Field(
        default="./credentials/credentials.json",
        description="Path to Gmail OAuth2 credentials.json file"
    )
    gmail_token_path: str = Field(
        default="./credentials/token.json",
        description="Path to store Gmail OAuth2 token (auto-created)"
    )

    # Application Configuration
    app_env: str = Field(
        default="development",
        description="Application environment (development, production)"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )

    @field_validator("llm_api_key", "brave_api_key")
    @classmethod
    def validate_api_keys(cls, v: str) -> str:
        """
        Ensure API keys are not empty.

        Args:
            v: API key value to validate

        Returns:
            str: Validated API key

        Raises:
            ValueError: If API key is empty or whitespace
        """
        if not v or v.strip() == "":
            raise ValueError("API key cannot be empty")
        return v.strip()


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    # For testing or initial setup, provide helpful error messages
    error_msg = str(e)
    if "llm_api_key" in error_msg.lower():
        error_msg = "LLM_API_KEY not set. Please configure it in .env file."
    elif "brave_api_key" in error_msg.lower():
        error_msg = "BRAVE_API_KEY not set. Please configure it in .env file."

    # Re-raise with more helpful message
    raise ValueError(f"Configuration error: {error_msg}") from e
