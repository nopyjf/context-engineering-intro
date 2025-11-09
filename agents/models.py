"""
Data models for the multi-agent system.

This module contains all Pydantic models and dataclasses used for:
- Research agent data structures
- Email agent data structures
- Dependency injection structures
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
# Import dependency classes for re-export
from .dependencies import ResearchAgentDependencies, EmailAgentDependencies

# Re-export dependencies for convenience
__all__ = [
    'BraveSearchResult',
    'ResearchQuery',
    'ResearchSummary',
    'EmailDraft',
    'GmailDraftResponse',
    'ResearchAgentDependencies',
    'EmailAgentDependencies',
]


# =============================================================================
# Research Agent Models
# =============================================================================

class BraveSearchResult(BaseModel):
    """
    Individual search result from Brave API.

    Attributes:
        title: Result title from search
        url: Result URL
        description: Result description/snippet
        score: Relevance score (0.0 to 1.0)
    """
    title: str = Field(..., description="Result title")
    url: str = Field(..., description="Result URL")
    description: str = Field(..., description="Result description/snippet")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")


class ResearchQuery(BaseModel):
    """
    Research query parameters.

    Attributes:
        query: Search query string
        max_results: Maximum results to return (1-20)
        include_summary: Whether to include research summary
    """
    query: str = Field(..., min_length=1, description="Search query")
    max_results: int = Field(
        10,
        ge=1,
        le=20,
        description="Maximum results to return"
    )
    include_summary: bool = Field(
        True,
        description="Include research summary"
    )


class ResearchSummary(BaseModel):
    """
    Structured research summary.

    Attributes:
        topic: Research topic
        key_findings: List of key findings from research
        sources: List of source URLs used
        summary_text: Human-readable summary
        timestamp: When the research was conducted
    """
    topic: str = Field(..., description="Research topic")
    key_findings: List[str] = Field(
        default_factory=list,
        description="Key findings"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Source URLs"
    )
    summary_text: str = Field(..., description="Human-readable summary")
    timestamp: datetime = Field(default_factory=datetime.now)


# =============================================================================
# Email Agent Models
# =============================================================================

class EmailDraft(BaseModel):
    """
    Email draft structure for Gmail.

    Attributes:
        recipient: Recipient email address
        subject: Email subject line
        body: Email body content
        cc: Optional CC recipients
        bcc: Optional BCC recipients
    """
    recipient: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None


class GmailDraftResponse(BaseModel):
    """
    Response from Gmail API after draft creation.

    Attributes:
        draft_id: Gmail draft ID
        message_id: Gmail message ID
        thread_id: Gmail thread ID
    """
    draft_id: str = Field(..., description="Gmail draft ID")
    message_id: str = Field(..., description="Gmail message ID")
    thread_id: str = Field(..., description="Gmail thread ID")
