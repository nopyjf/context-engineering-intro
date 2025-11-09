"""
Research Agent with multi-agent capabilities.

This module defines the primary Research Agent that can:
- Search the web using Brave Search API
- Synthesize research findings
- Delegate email drafting to Email Draft Agent
"""

from typing import Optional, List, Dict, Any
from pydantic_ai import Agent, RunContext
from .models import ResearchAgentDependencies, EmailAgentDependencies
from .prompts import RESEARCH_AGENT_PROMPT
from .providers import get_llm_model
from .tools import search_web_tool
from .email_agent import email_agent


# Initialize the Research Agent
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,
    system_prompt=RESEARCH_AGENT_PROMPT
)


@research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API.

    This tool searches for information on the web and returns relevant
    results with titles, URLs, descriptions, and relevance scores.

    Args:
        ctx: Agent runtime context with dependencies
        query: Search query string
        max_results: Maximum number of results to return (1-20)

    Returns:
        List of search results with structured data
    """
    # Validate max_results range
    max_results = min(max(max_results, 1), 20)

    try:
        # Extract Brave API key from dependencies
        brave_api_key = ctx.deps.brave_api_key

        # Call the search tool
        results = await search_web_tool(
            api_key=brave_api_key,
            query=query,
            count=max_results
        )

        return results

    except Exception as e:
        # Return error information in a structured format
        return [{
            "title": "Search Error",
            "url": "",
            "description": f"Failed to search: {str(e)}",
            "score": 0.0
        }]


@research_agent.tool
async def create_email_draft(
    ctx: RunContext[ResearchAgentDependencies],
    recipient_email: str,
    subject: str,
    context: str,
    research_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create email draft using Email Agent (agent-as-tool pattern).

    This tool delegates email composition to a specialized Email Agent,
    passing research context and findings for professional email drafting.

    CRITICAL: Must pass ctx.usage for token tracking across agents.

    Args:
        ctx: Agent runtime context with dependencies
        recipient_email: Email address of recipient
        subject: Email subject line
        context: Context for the email
        research_summary: Optional research findings to include

    Returns:
        Dictionary with email creation status and details
    """
    try:
        # Build comprehensive prompt for email agent
        if research_summary:
            email_prompt = f"""
Create a professional email to {recipient_email} with subject "{subject}".

Context: {context}

Research Summary:
{research_summary}

Please create a well-structured email that:
1. Has an appropriate greeting
2. Provides clear context
3. Summarizes key research findings professionally
4. Includes actionable next steps if appropriate
5. Ends with a professional closing

Maintain a professional yet friendly tone.
"""
        else:
            email_prompt = f"""
Create a professional email to {recipient_email} with subject "{subject}".

Context: {context}
"""

        # Create dependencies for email agent from parent deps
        email_deps = EmailAgentDependencies(
            gmail_credentials_path=ctx.deps.gmail_credentials_path,
            gmail_token_path=ctx.deps.gmail_token_path,
            session_id=ctx.deps.session_id
        )

        # CRITICAL: Pass usage=ctx.usage for token tracking
        # This ensures tokens are tracked across the entire multi-agent conversation
        result = await email_agent.run(
            email_prompt,
            deps=email_deps,
            usage=ctx.usage  # Token tracking
        )

        return {
            "success": True,
            "agent_response": result.data,
            "recipient": recipient_email,
            "subject": subject,
            "context": context
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create email draft: {str(e)}"
        }


@research_agent.tool
async def summarize_research(
    ctx: RunContext[ResearchAgentDependencies],
    search_results: List[Dict[str, Any]],
    topic: str,
    focus_areas: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Summarize research findings from search results.

    This tool extracts key information from search results and creates
    a structured summary with sources and key findings.

    Args:
        ctx: Agent runtime context with dependencies
        search_results: List of search results to summarize
        topic: Research topic
        focus_areas: Optional specific areas to focus on

    Returns:
        Dictionary with structured research summary
    """
    try:
        # Extract key information from search results
        sources = []
        descriptions = []

        for result in search_results:
            if isinstance(result, dict):
                url = result.get("url", "")
                title = result.get("title", "")
                description = result.get("description", "")

                if url:
                    sources.append(f"{title}: {url}")
                if description:
                    descriptions.append(description)

        # Create summary text
        summary_parts = [
            f"Research Summary on: {topic}",
            "",
            "Key Findings:",
        ]

        for i, desc in enumerate(descriptions[:5], 1):
            summary_parts.append(f"{i}. {desc}")

        summary_parts.append("")
        summary_parts.append("Sources:")

        for i, source in enumerate(sources[:5], 1):
            summary_parts.append(f"{i}. {source}")

        if focus_areas:
            summary_parts.append("")
            summary_parts.append(f"Focus Areas: {', '.join(focus_areas)}")

        summary_text = "\n".join(summary_parts)

        return {
            "topic": topic,
            "key_findings": descriptions[:5],
            "sources": sources[:5],
            "summary_text": summary_text,
            "result_count": len(search_results)
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to summarize research: {str(e)}"
        }


def create_research_agent() -> Agent:
    """
    Convenience function to create and return a Research Agent instance.

    Returns:
        Configured Research Agent with all tools
    """
    return research_agent
