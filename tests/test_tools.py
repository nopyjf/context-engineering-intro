"""
Tests for tool functions (Brave Search and Gmail).

This module tests:
- Brave Search API integration
- Gmail API integration
- Error handling and edge cases
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from agents.tools import search_web_tool, create_gmail_draft_tool


# =============================================================================
# Brave Search Tool Tests
# =============================================================================

@pytest.mark.asyncio
async def test_search_web_happy_path(mock_brave_api_response):
    """Test Brave search returns valid results."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Create mock response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_brave_api_response
        mock_get.return_value = mock_response

        # Call the tool
        results = await search_web_tool(
            api_key="test_key",
            query="test query",
            count=10
        )

        # Assertions
        assert len(results) == 3
        assert results[0]["title"] == "Test Result 1"
        assert results[0]["url"] == "https://example.com/result1"
        assert results[0]["score"] > 0
        assert results[0]["score"] <= 1.0


@pytest.mark.asyncio
async def test_search_web_rate_limit():
    """Test handling of Brave API rate limit."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Create mock response for rate limit
        mock_response = AsyncMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        # Should raise exception
        with pytest.raises(Exception) as exc_info:
            await search_web_tool(api_key="test_key", query="test")

        assert "rate limit" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_search_web_invalid_key():
    """Test handling of invalid Brave API key."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Create mock response for invalid key
        mock_response = AsyncMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        # Should raise exception
        with pytest.raises(Exception) as exc_info:
            await search_web_tool(api_key="invalid", query="test")

        assert "invalid" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_search_web_empty_query():
    """Test validation of empty query."""
    with pytest.raises(ValueError) as exc_info:
        await search_web_tool(api_key="key", query="")

    assert "empty" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_search_web_empty_api_key():
    """Test validation of empty API key."""
    with pytest.raises(ValueError) as exc_info:
        await search_web_tool(api_key="", query="test query")

    assert "required" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_search_web_count_validation():
    """Test that count parameter is validated to 1-20 range."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        mock_get.return_value = mock_response

        # Test count > 20 is clamped to 20
        await search_web_tool(api_key="key", query="test", count=50)

        # Check the call was made with count=20
        call_args = mock_get.call_args
        assert call_args[1]['params']['count'] == 20

        # Test count < 1 is clamped to 1
        await search_web_tool(api_key="key", query="test", count=0)

        # Check the call was made with count=1
        call_args = mock_get.call_args
        assert call_args[1]['params']['count'] == 1


# =============================================================================
# Gmail Tool Tests
# =============================================================================

@pytest.mark.asyncio
async def test_create_gmail_draft_success(mock_gmail_api_response, tmp_path):
    """Test successful Gmail draft creation."""
    # Create temporary credential files
    creds_file = tmp_path / "credentials.json"
    token_file = tmp_path / "token.json"

    # Create dummy credentials
    creds_file.write_text('{"installed": {"client_id": "test"}}')

    with patch('agents.tools.Credentials') as mock_creds_class:
        with patch('agents.tools.build') as mock_build:
            # Mock credentials
            mock_creds = MagicMock()
            mock_creds.valid = True
            mock_creds.expired = False
            mock_creds_class.from_authorized_user_file.return_value = mock_creds

            # Mock Gmail service
            mock_service = MagicMock()
            mock_drafts = MagicMock()
            mock_drafts.create.return_value.execute.return_value = mock_gmail_api_response
            mock_service.users.return_value.drafts.return_value = mock_drafts
            mock_build.return_value = mock_service

            # Create token file to avoid OAuth flow
            token_file.write_text('{"token": "test_token"}')

            # Call the tool
            result = await create_gmail_draft_tool(
                credentials_path=str(creds_file),
                token_path=str(token_file),
                recipient="test@example.com",
                subject="Test Subject",
                body="Test body content"
            )

            # Assertions
            assert result["draft_id"] == "draft_123456"
            assert result["message_id"] == "msg_123456"
            assert result["thread_id"] == "thread_123456"


@pytest.mark.asyncio
async def test_create_gmail_draft_missing_credentials():
    """Test error handling when credentials file is missing."""
    with pytest.raises(Exception) as exc_info:
        await create_gmail_draft_tool(
            credentials_path="/nonexistent/credentials.json",
            token_path="/nonexistent/token.json",
            recipient="test@example.com",
            subject="Test",
            body="Test body"
        )

    assert "credentials not found" in str(exc_info.value).lower()


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================

@pytest.mark.asyncio
async def test_search_web_network_error():
    """Test handling of network errors."""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Simulate network error
        import httpx
        mock_get.side_effect = httpx.RequestError("Network error")

        with pytest.raises(Exception) as exc_info:
            await search_web_tool(api_key="key", query="test")

        assert "request failed" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_search_web_empty_results(mock_brave_api_response):
    """Test handling of empty search results."""
    # Modify response to have empty results
    empty_response = {"web": {"results": []}}

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = empty_response
        mock_get.return_value = mock_response

        results = await search_web_tool(
            api_key="test_key",
            query="obscure query",
            count=10
        )

        # Should return empty list
        assert len(results) == 0
        assert isinstance(results, list)
