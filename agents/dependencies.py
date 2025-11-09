"""
Dependency injection structures for the multi-agent system.

This module defines dataclasses used for dependency injection in agents.
These dependencies provide agents with access to external services and
configuration at runtime.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchAgentDependencies:
    """
    Dependencies for Research Agent execution.

    The Research Agent requires access to:
    - Brave Search API for web search
    - Gmail credentials for email draft creation
    - Session tracking (optional)

    Attributes:
        brave_api_key: Brave Search API key for web search
        gmail_credentials_path: Path to Gmail OAuth2 credentials.json
        gmail_token_path: Path to Gmail OAuth2 token storage (auto-created)
        session_id: Optional session identifier for tracking conversations
    """
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None


@dataclass
class EmailAgentDependencies:
    """
    Dependencies for Email Agent execution.

    The Email Agent requires access to:
    - Gmail credentials for draft creation
    - Session tracking (optional)

    Attributes:
        gmail_credentials_path: Path to Gmail OAuth2 credentials.json
        gmail_token_path: Path to Gmail OAuth2 token storage (auto-created)
        session_id: Optional session identifier for tracking conversations
    """
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None
