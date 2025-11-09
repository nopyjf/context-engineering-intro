"""
Tool functions for the multi-agent system.

This module contains pure async functions for:
- Brave Search API integration
- Gmail API integration for draft creation
"""

import os
import base64
from typing import List, Dict, Any
from email.mime.text import MIMEText
import httpx
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# =============================================================================
# Brave Search Tool
# =============================================================================

async def search_web_tool(
    api_key: str,
    query: str,
    count: int = 10,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API.

    This is a pure async function that will be wrapped by agent tool decorator.

    Args:
        api_key: Brave Search API key
        query: Search query string
        count: Number of results to return (1-20)
        offset: Result offset for pagination

    Returns:
        List of search results with title, url, description, and score

    Raises:
        ValueError: If inputs are invalid
        Exception: If API call fails (rate limit, auth error, network error)
    """
    # Validate inputs before API call to avoid wasting quota
    if not api_key or not api_key.strip():
        raise ValueError("Brave API key is required")

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    # Brave API only accepts count 1-20
    count = min(max(count, 1), 20)

    headers = {
        "X-Subscription-Token": api_key,  # Header name for Brave API
        "Accept": "application/json"
    }

    params = {"q": query, "count": count, "offset": offset}

    # Use httpx AsyncClient for async HTTP
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=30.0  # Prevent hanging
            )

            # Brave returns 429 on rate limit (2000/month free tier)
            if response.status_code == 429:
                raise Exception(
                    "Brave API rate limit exceeded. "
                    "Check your monthly quota at brave.com/search/api/"
                )

            # Returns 401 for invalid key
            if response.status_code == 401:
                raise Exception(
                    "Invalid Brave API key. "
                    "Verify your API key at brave.com/search/api/"
                )

            if response.status_code != 200:
                raise Exception(
                    f"Brave API error {response.status_code}: {response.text}"
                )

            data = response.json()

            # Brave response structure: {"web": {"results": [...]}}
            web_results = data.get("web", {}).get("results", [])

            # Convert to standardized format
            results = []
            for idx, result in enumerate(web_results):
                # Calculate relevance score (simple position-based)
                score = 1.0 - (idx * 0.05)
                score = max(score, 0.1)

                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "score": score
                })

            return results

        except httpx.RequestError as e:
            # Convert HTTP errors to user-friendly messages
            raise Exception(f"Request failed: {str(e)}")


# =============================================================================
# Gmail Tool
# =============================================================================

# Gmail API scope for draft creation
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


async def create_gmail_draft_tool(
    credentials_path: str,
    token_path: str,
    recipient: str,
    subject: str,
    body: str
) -> Dict[str, Any]:
    """
    Create Gmail draft with OAuth2 authentication.

    This function handles the OAuth2 flow on first use and creates
    a draft email in the user's Gmail account.

    Args:
        credentials_path: Path to credentials.json from Google Cloud Console
        token_path: Path where token.json will be stored (auto-created)
        recipient: Recipient email address
        subject: Email subject line
        body: Email body content

    Returns:
        Dictionary with draft_id, message_id, and thread_id

    Raises:
        Exception: If OAuth flow fails or draft creation fails
    """
    creds = None

    # Check for existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, GMAIL_SCOPES)

    # Token might be expired, refresh if needed
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # If no valid credentials, run OAuth flow (opens browser)
    if not creds or not creds.valid:
        if not os.path.exists(credentials_path):
            raise Exception(
                f"Gmail credentials not found at {credentials_path}. "
                f"Please download credentials.json from Google Cloud Console."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, GMAIL_SCOPES
        )
        # This opens a browser for user authorization
        creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Create MIME message (RFC 2822 format)
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject

    # Gmail API requires base64url encoding (no padding)
    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode('utf-8')

    # Create draft via Gmail API
    draft = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw_message}}
    ).execute()

    # Return structured response
    return {
        "draft_id": draft['id'],
        "message_id": draft['message']['id'],
        "thread_id": draft['message'].get('threadId', '')
    }
