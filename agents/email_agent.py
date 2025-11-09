"""
Email Draft Agent for creating professional Gmail drafts.

This module defines an agent specialized in composing and creating
email drafts in Gmail based on provided context and requirements.
"""

from pydantic_ai import Agent, RunContext
from .models import EmailAgentDependencies
from .prompts import EMAIL_AGENT_PROMPT
from .providers import get_llm_model
from .tools import create_gmail_draft_tool


# Initialize the Email Draft Agent
email_agent = Agent(
    get_llm_model(),
    deps_type=EmailAgentDependencies,
    system_prompt=EMAIL_AGENT_PROMPT
)


@email_agent.tool
async def create_gmail_draft(
    ctx: RunContext[EmailAgentDependencies],
    recipient: str,
    subject: str,
    body: str
) -> dict:
    """
    Create a Gmail draft with the provided content.

    This tool uses the Gmail API to create a draft email in the user's
    Gmail account. The draft can be reviewed and edited before sending.

    Args:
        ctx: Agent runtime context with dependencies
        recipient: Recipient email address
        subject: Email subject line
        body: Complete email body content

    Returns:
        Dictionary with success status and draft details
    """
    try:
        # Extract Gmail configuration from dependencies
        credentials_path = ctx.deps.gmail_credentials_path
        token_path = ctx.deps.gmail_token_path

        # Create the Gmail draft
        result = await create_gmail_draft_tool(
            credentials_path=credentials_path,
            token_path=token_path,
            recipient=recipient,
            subject=subject,
            body=body
        )

        return {
            "success": True,
            "message": f"Gmail draft created successfully for {recipient}",
            "draft_id": result["draft_id"],
            "message_id": result["message_id"],
            "thread_id": result["thread_id"]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create Gmail draft: {str(e)}"
        }


def create_email_agent() -> Agent:
    """
    Convenience function to create and return an Email Agent instance.

    Returns:
        Configured Email Draft Agent
    """
    return email_agent
