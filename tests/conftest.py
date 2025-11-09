"""
Pytest configuration and fixtures for test suite.

This module provides:
- Mock settings
- Mock API responses
- Sample test data
- Common fixtures for testing
"""

import pytest
import os
import sys
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.dependencies import ResearchAgentDependencies, EmailAgentDependencies


@pytest.fixture
def mock_settings(monkeypatch):
    """
    Mock settings with test values.

    Returns:
        Mock settings object with test configuration
    """
    # Set test environment variables
    monkeypatch.setenv("LLM_API_KEY", "test_llm_key")
    monkeypatch.setenv("BRAVE_API_KEY", "test_brave_key")
    monkeypatch.setenv("LLM_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    # Re-import settings after setting environment variables
    from agents import settings
    return settings


@pytest.fixture
def mock_brave_api_response() -> Dict[str, Any]:
    """
    Mock Brave Search API response.

    Returns:
        Dictionary mimicking Brave API response structure
    """
    return {
        "web": {
            "results": [
                {
                    "title": "Test Result 1",
                    "url": "https://example.com/result1",
                    "description": "This is a test search result description"
                },
                {
                    "title": "Test Result 2",
                    "url": "https://example.com/result2",
                    "description": "Another test search result"
                },
                {
                    "title": "Test Result 3",
                    "url": "https://example.com/result3",
                    "description": "Third test result for completeness"
                }
            ]
        }
    }


@pytest.fixture
def mock_gmail_api_response() -> Dict[str, Any]:
    """
    Mock Gmail API response for draft creation.

    Returns:
        Dictionary mimicking Gmail API draft response
    """
    return {
        "id": "draft_123456",
        "message": {
            "id": "msg_123456",
            "threadId": "thread_123456"
        }
    }


@pytest.fixture
def sample_search_results() -> List[Dict[str, Any]]:
    """
    Sample search results for testing.

    Returns:
        List of search result dictionaries
    """
    return [
        {
            "title": "AI Research Paper",
            "url": "https://example.com/ai-paper",
            "description": "A comprehensive study on artificial intelligence",
            "score": 1.0
        },
        {
            "title": "Machine Learning Tutorial",
            "url": "https://example.com/ml-tutorial",
            "description": "Learn machine learning basics",
            "score": 0.95
        },
        {
            "title": "Data Science Guide",
            "url": "https://example.com/ds-guide",
            "description": "Complete guide to data science",
            "score": 0.90
        }
    ]


@pytest.fixture
def sample_email_draft() -> Dict[str, str]:
    """
    Sample email draft data.

    Returns:
        Dictionary with email draft fields
    """
    return {
        "recipient": "test@example.com",
        "subject": "Test Email Subject",
        "body": "This is a test email body with important information."
    }


@pytest.fixture
def research_agent_deps() -> ResearchAgentDependencies:
    """
    Create test dependencies for Research Agent.

    Returns:
        ResearchAgentDependencies with test values
    """
    return ResearchAgentDependencies(
        brave_api_key="test_brave_key",
        gmail_credentials_path="./test_credentials.json",
        gmail_token_path="./test_token.json",
        session_id="test_session"
    )


@pytest.fixture
def email_agent_deps() -> EmailAgentDependencies:
    """
    Create test dependencies for Email Agent.

    Returns:
        EmailAgentDependencies with test values
    """
    return EmailAgentDependencies(
        gmail_credentials_path="./test_credentials.json",
        gmail_token_path="./test_token.json",
        session_id="test_session"
    )
