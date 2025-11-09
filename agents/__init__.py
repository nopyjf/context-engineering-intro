"""
Multi-Agent System Package

This package contains a production-ready multi-agent system with:
- Research Agent: Web search and research synthesis
- Email Agent: Professional Gmail draft creation
- Tool integrations: Brave Search API and Gmail API

Usage:
    from agents import research_agent, email_agent
    from agents import ResearchAgentDependencies, EmailAgentDependencies
"""

# Import main agents
from .research_agent import research_agent, create_research_agent
from .email_agent import email_agent, create_email_agent

# Import dependency classes
from .dependencies import (
    ResearchAgentDependencies,
    EmailAgentDependencies,
)

# Import models
from .models import (
    BraveSearchResult,
    ResearchQuery,
    ResearchSummary,
    EmailDraft,
    GmailDraftResponse,
)

# Import settings and providers
from .settings import settings
from .providers import get_llm_model, get_model_info

__all__ = [
    # Agents
    'research_agent',
    'email_agent',
    'create_research_agent',
    'create_email_agent',
    # Dependencies
    'ResearchAgentDependencies',
    'EmailAgentDependencies',
    # Models
    'BraveSearchResult',
    'ResearchQuery',
    'ResearchSummary',
    'EmailDraft',
    'GmailDraftResponse',
    # Configuration
    'settings',
    'get_llm_model',
    'get_model_info',
]

__version__ = '1.0.0'
