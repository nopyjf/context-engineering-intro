"""
Tests for dependency structures.

This module tests:
- Dependency dataclasses
- Dependency injection patterns
- Settings validation
"""

import pytest
from agents.dependencies import ResearchAgentDependencies, EmailAgentDependencies
from agents.settings import Settings
from pydantic import ValidationError


def test_research_agent_dependencies_creation():
    """Test ResearchAgentDependencies can be created with required fields."""
    deps = ResearchAgentDependencies(
        brave_api_key="test_key",
        gmail_credentials_path="/path/to/creds.json",
        gmail_token_path="/path/to/token.json"
    )

    assert deps.brave_api_key == "test_key"
    assert deps.gmail_credentials_path == "/path/to/creds.json"
    assert deps.gmail_token_path == "/path/to/token.json"
    assert deps.session_id is None  # Default value


def test_research_agent_dependencies_with_session():
    """Test ResearchAgentDependencies with optional session_id."""
    deps = ResearchAgentDependencies(
        brave_api_key="test_key",
        gmail_credentials_path="/path/to/creds.json",
        gmail_token_path="/path/to/token.json",
        session_id="session_123"
    )

    assert deps.session_id == "session_123"


def test_email_agent_dependencies_creation():
    """Test EmailAgentDependencies can be created with required fields."""
    deps = EmailAgentDependencies(
        gmail_credentials_path="/path/to/creds.json",
        gmail_token_path="/path/to/token.json"
    )

    assert deps.gmail_credentials_path == "/path/to/creds.json"
    assert deps.gmail_token_path == "/path/to/token.json"
    assert deps.session_id is None


def test_email_agent_dependencies_with_session():
    """Test EmailAgentDependencies with optional session_id."""
    deps = EmailAgentDependencies(
        gmail_credentials_path="/path/to/creds.json",
        gmail_token_path="/path/to/token.json",
        session_id="session_456"
    )

    assert deps.session_id == "session_456"


def test_settings_validation_requires_api_keys(monkeypatch):
    """Test that Settings validation requires API keys."""
    # Clear environment variables
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)

    # Should raise validation error
    with pytest.raises(Exception):  # Could be ValidationError or ValueError
        Settings()


def test_settings_validation_empty_api_key(monkeypatch):
    """Test that empty API keys are rejected."""
    monkeypatch.setenv("LLM_API_KEY", "")
    monkeypatch.setenv("BRAVE_API_KEY", "valid_key")

    with pytest.raises(Exception):
        Settings()


def test_settings_with_valid_values(monkeypatch):
    """Test Settings with all valid values."""
    monkeypatch.setenv("LLM_API_KEY", "llm_test_key")
    monkeypatch.setenv("BRAVE_API_KEY", "brave_test_key")
    monkeypatch.setenv("LLM_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    settings = Settings()

    assert settings.llm_api_key == "llm_test_key"
    assert settings.brave_api_key == "brave_test_key"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.llm_provider == "openai"


def test_settings_default_values(monkeypatch):
    """Test that Settings uses default values for optional fields."""
    monkeypatch.setenv("LLM_API_KEY", "test_key")
    monkeypatch.setenv("BRAVE_API_KEY", "test_key")

    settings = Settings()

    # Check defaults
    assert settings.llm_provider == "openai"
    assert settings.llm_model == "gpt-4o-mini"
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.debug is False


def test_dependency_immutability():
    """Test that dependencies behave as expected dataclasses."""
    deps = ResearchAgentDependencies(
        brave_api_key="key1",
        gmail_credentials_path="/path1",
        gmail_token_path="/path2"
    )

    # Should be able to access attributes
    assert deps.brave_api_key == "key1"

    # Dataclasses are mutable by default, but attributes should be accessible
    deps.session_id = "new_session"
    assert deps.session_id == "new_session"
