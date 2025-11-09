"""
Integration tests for multi-agent system.

This module tests:
- End-to-end workflows
- Multi-agent communication
- Token usage tracking
- Conversation flows
"""

import pytest
from pydantic_ai.models.test import TestModel
from agents.research_agent import research_agent
from agents.email_agent import email_agent
from agents.dependencies import ResearchAgentDependencies, EmailAgentDependencies


@pytest.mark.asyncio
async def test_research_to_email_flow(research_agent_deps):
    """Test complete flow: research query -> email draft."""
    from unittest.mock import patch

    # Override both agents with TestModel
    test_research = research_agent.override(model=TestModel())
    test_email = email_agent.override(model=TestModel())

    # Mock the email_agent in research_agent module
    with patch('agents.research_agent.email_agent', test_email):
        # Mock search results
        with patch('agents.research_agent.search_web_tool') as mock_search:
            mock_search.return_value = [
                {
                    "title": "AI Safety Research",
                    "url": "https://example.com/ai-safety",
                    "description": "Important findings on AI safety",
                    "score": 1.0
                }
            ]

            # Run the research agent
            result = await test_research.run(
                "Research AI safety and create an email to test@example.com",
                deps=research_agent_deps
            )

            # Verify we got a result
            assert result.data is not None


@pytest.mark.asyncio
async def test_multi_agent_token_tracking(research_agent_deps):
    """Test that token usage is tracked across agents."""
    # This test verifies the pattern of passing ctx.usage
    # In real usage, tokens would accumulate across agent calls
    test_research = research_agent.override(model=TestModel())

    # Run with usage tracking
    result = await test_research.run(
        "Test query",
        deps=research_agent_deps
    )

    # Verify result has usage information
    assert hasattr(result, 'usage')
    # Note: TestModel doesn't actually consume tokens, but structure is there


@pytest.mark.asyncio
async def test_conversation_history_handling(research_agent_deps):
    """Test that conversation history is maintained."""
    test_research = research_agent.override(model=TestModel())

    # Simulate multiple turns
    messages = [
        "What is machine learning?",
        "Can you explain it more simply?",
        "Give me an example"
    ]

    results = []
    for message in messages:
        result = await test_research.run(
            message,
            deps=research_agent_deps
        )
        results.append(result.data)

    # Verify all messages were processed
    assert len(results) == len(messages)
    for result in results:
        assert result is not None


@pytest.mark.asyncio
async def test_multi_agent_dependency_passing():
    """Test that dependencies are correctly passed between agents."""
    from unittest.mock import patch, MagicMock

    # Create research dependencies
    research_deps = ResearchAgentDependencies(
        brave_api_key="test_brave",
        gmail_credentials_path="/test/creds.json",
        gmail_token_path="/test/token.json",
        session_id="test_session"
    )

    # Get the create_email_draft tool
    email_tool = None
    for tool in research_agent._tools_list:
        if tool.name == "create_email_draft":
            email_tool = tool
            break

    assert email_tool is not None

    # Mock the email agent run
    with patch('agents.research_agent.email_agent') as mock_email_agent:
        mock_result = MagicMock()
        mock_result.data = "Email created"
        mock_email_agent.run.return_value = mock_result

        # Create mock context with usage
        mock_ctx = MagicMock()
        mock_ctx.deps = research_deps
        mock_ctx.usage = MagicMock()

        # Call the tool
        result = await email_tool.function(
            mock_ctx,
            recipient_email="test@example.com",
            subject="Test",
            context="Test context"
        )

        # Verify email agent was called with correct dependencies
        assert mock_email_agent.run.called
        call_kwargs = mock_email_agent.run.call_args[1]

        # Verify EmailAgentDependencies were created correctly
        email_deps = call_kwargs['deps']
        assert email_deps.gmail_credentials_path == "/test/creds.json"
        assert email_deps.gmail_token_path == "/test/token.json"
        assert email_deps.session_id == "test_session"

        # CRITICAL: Verify usage was passed for token tracking
        assert 'usage' in call_kwargs
        assert call_kwargs['usage'] == mock_ctx.usage


@pytest.mark.asyncio
async def test_error_propagation(research_agent_deps):
    """Test that errors are handled and propagated correctly."""
    from unittest.mock import patch

    test_research = research_agent.override(model=TestModel())

    # Mock search to raise an error
    with patch('agents.research_agent.search_web_tool') as mock_search:
        mock_search.side_effect = Exception("API Error")

        # The agent should handle the error gracefully
        # (tools return error messages in structured format)
        result = await test_research.run(
            "Search for something",
            deps=research_agent_deps
        )

        # Should still get a result, even if tools failed
        assert result.data is not None
