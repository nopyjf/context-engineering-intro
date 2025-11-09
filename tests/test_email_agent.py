"""
Tests for Email Agent.

This module tests:
- Email agent initialization
- Tool registration
- Draft creation functionality
- Error handling
"""

import pytest
from pydantic_ai.models.test import TestModel
from agents.email_agent import email_agent
from agents.dependencies import EmailAgentDependencies


@pytest.mark.asyncio
async def test_email_agent_initialization():
    """Test email agent initializes correctly."""
    assert email_agent is not None
    assert email_agent.deps_type == EmailAgentDependencies


@pytest.mark.asyncio
async def test_email_agent_with_test_model(email_agent_deps):
    """Test email agent with TestModel (no API calls)."""
    # Override with TestModel
    test_agent = email_agent.override(model=TestModel())

    # Run the agent
    result = await test_agent.run(
        "Create an email to john@example.com about project updates",
        deps=email_agent_deps
    )

    # TestModel returns simple responses
    assert result.data is not None
    assert isinstance(result.data, str)


@pytest.mark.asyncio
async def test_email_agent_tools_registered():
    """Test that create_gmail_draft tool is registered."""
    # Get tool names
    tool_names = [tool.name for tool in email_agent._tools_list]

    # Verify expected tool is registered
    assert "create_gmail_draft" in tool_names


@pytest.mark.asyncio
async def test_create_gmail_draft_tool_success(email_agent_deps):
    """Test create_gmail_draft tool with mocked Gmail API."""
    from unittest.mock import patch, AsyncMock

    # Mock the create_gmail_draft_tool function
    with patch('agents.email_agent.create_gmail_draft_tool') as mock_gmail:
        # Set up mock return value
        mock_gmail.return_value = {
            "draft_id": "draft_123",
            "message_id": "msg_123",
            "thread_id": "thread_123"
        }

        # Get the tool function
        draft_tool = None
        for tool in email_agent._tools_list:
            if tool.name == "create_gmail_draft":
                draft_tool = tool
                break

        assert draft_tool is not None

        # Create a mock context
        from unittest.mock import MagicMock
        mock_ctx = MagicMock()
        mock_ctx.deps = email_agent_deps

        # Call the tool directly
        result = await draft_tool.function(
            mock_ctx,
            recipient="test@example.com",
            subject="Test Subject",
            body="Test email body"
        )

        # Verify result
        assert isinstance(result, dict)
        assert result["success"] is True
        assert "draft_id" in result


@pytest.mark.asyncio
async def test_create_gmail_draft_tool_error(email_agent_deps):
    """Test create_gmail_draft tool error handling."""
    from unittest.mock import patch

    # Mock the create_gmail_draft_tool to raise an exception
    with patch('agents.email_agent.create_gmail_draft_tool') as mock_gmail:
        mock_gmail.side_effect = Exception("Gmail API Error")

        # Get the tool
        draft_tool = None
        for tool in email_agent._tools_list:
            if tool.name == "create_gmail_draft":
                draft_tool = tool
                break

        # Create mock context
        from unittest.mock import MagicMock
        mock_ctx = MagicMock()
        mock_ctx.deps = email_agent_deps

        # Call should handle error gracefully
        result = await draft_tool.function(
            mock_ctx,
            recipient="test@example.com",
            subject="Test",
            body="Test body"
        )

        # Should return error in structured format
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result


@pytest.mark.asyncio
async def test_email_validation():
    """Test email field validation with Pydantic models."""
    from agents.models import EmailDraft
    from pydantic import ValidationError

    # Valid email
    valid_draft = EmailDraft(
        recipient="test@example.com",
        subject="Test Subject",
        body="Test body content"
    )
    assert valid_draft.recipient == "test@example.com"

    # Invalid email should raise validation error
    with pytest.raises(ValidationError):
        EmailDraft(
            recipient="invalid-email",
            subject="Test",
            body="Test body"
        )
