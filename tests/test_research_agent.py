"""
Tests for Research Agent.

This module tests:
- Research agent initialization
- Tool registration
- Agent responses with TestModel
- Error handling
"""

import pytest
from pydantic_ai.models.test import TestModel
from agents.research_agent import research_agent
from agents.dependencies import ResearchAgentDependencies


@pytest.mark.asyncio
async def test_research_agent_initialization():
    """Test research agent initializes correctly."""
    assert research_agent is not None
    assert research_agent.deps_type == ResearchAgentDependencies


@pytest.mark.asyncio
async def test_research_agent_with_test_model(research_agent_deps):
    """Test research agent with TestModel (no API calls)."""
    # Override with TestModel to avoid API calls
    test_agent = research_agent.override(model=TestModel())

    # Run the agent with test dependencies
    result = await test_agent.run(
        "Tell me about artificial intelligence",
        deps=research_agent_deps
    )

    # TestModel returns simple responses
    assert result.data is not None
    assert isinstance(result.data, str)


@pytest.mark.asyncio
async def test_research_agent_tools_registered():
    """Test that all required tools are registered."""
    # Get tool names
    tool_names = [tool.name for tool in research_agent._tools_list]

    # Verify expected tools are registered
    assert "search_web" in tool_names
    assert "create_email_draft" in tool_names
    assert "summarize_research" in tool_names


@pytest.mark.asyncio
async def test_search_web_tool_with_mock(research_agent_deps):
    """Test search_web tool with mocked responses."""
    from unittest.mock import patch, AsyncMock

    # Mock the search_web_tool function
    with patch('agents.research_agent.search_web_tool') as mock_search:
        # Set up mock return value
        mock_search.return_value = [
            {
                "title": "Test Result",
                "url": "https://test.com",
                "description": "Test description",
                "score": 1.0
            }
        ]

        # Get the tool function
        search_tool = None
        for tool in research_agent._tools_list:
            if tool.name == "search_web":
                search_tool = tool
                break

        assert search_tool is not None

        # Create a mock context
        from unittest.mock import MagicMock
        mock_ctx = MagicMock()
        mock_ctx.deps = research_agent_deps

        # Call the tool directly
        result = await search_tool.function(
            mock_ctx,
            query="test query",
            max_results=10
        )

        # Verify result
        assert isinstance(result, list)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_summarize_research_tool(research_agent_deps, sample_search_results):
    """Test summarize_research tool."""
    # Get the tool function
    summarize_tool = None
    for tool in research_agent._tools_list:
        if tool.name == "summarize_research":
            summarize_tool = tool
            break

    assert summarize_tool is not None

    # Create a mock context
    from unittest.mock import MagicMock
    mock_ctx = MagicMock()
    mock_ctx.deps = research_agent_deps

    # Call the tool
    result = await summarize_tool.function(
        mock_ctx,
        search_results=sample_search_results,
        topic="AI Research"
    )

    # Verify result structure
    assert isinstance(result, dict)
    assert "topic" in result
    assert "key_findings" in result
    assert "sources" in result
    assert result["topic"] == "AI Research"


@pytest.mark.asyncio
async def test_research_agent_error_handling(research_agent_deps):
    """Test research agent handles errors gracefully."""
    from unittest.mock import patch

    # Mock search_web_tool to raise an exception
    with patch('agents.research_agent.search_web_tool') as mock_search:
        mock_search.side_effect = Exception("API Error")

        # Get the tool
        search_tool = None
        for tool in research_agent._tools_list:
            if tool.name == "search_web":
                search_tool = tool
                break

        # Create mock context
        from unittest.mock import MagicMock
        mock_ctx = MagicMock()
        mock_ctx.deps = research_agent_deps

        # Call should handle error gracefully
        result = await search_tool.function(
            mock_ctx,
            query="test",
            max_results=10
        )

        # Should return error in structured format
        assert isinstance(result, list)
        assert len(result) > 0
        assert "error" in result[0]["title"].lower()
