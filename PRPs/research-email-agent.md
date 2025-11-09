name: "Multi-Agent System: Research Agent with Email Draft Sub-Agent"
description: |

## Purpose
Build a production-ready Pydantic AI multi-agent system where a primary Research Agent (using Brave Search API) can delegate email drafting tasks to an Email Draft Agent (using Gmail API). This demonstrates the agent-as-tool pattern with external API integrations and CLI interface for user interaction.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a production-ready multi-agent system where users can research topics via CLI, and the Research Agent can delegate email drafting tasks to an Email Draft Agent. The system should support multiple LLM providers, handle API authentication securely, and provide real-time streaming responses with tool visibility.

## Why
- **Business value**: Automates research and email drafting workflows, reducing manual effort
- **Integration**: Demonstrates advanced Pydantic AI multi-agent patterns with real-world APIs
- **User impact**: Enables users to quickly research topics and draft professional emails based on findings
- **Problems solved**:
  - Reduces time spent on research-based communications
  - Ensures professional email formatting with research context
  - Demonstrates best practices for multi-agent systems

## What
A CLI-based application where:
- Users input research queries or requests via an interactive CLI
- Research Agent searches using Brave Search API for relevant information
- Research Agent can invoke Email Draft Agent to create Gmail drafts based on research findings
- Results stream back to the user in real-time with full tool execution visibility
- Both agents work asynchronously with proper dependency injection
- Comprehensive error handling and validation

### Success Criteria
- [ ] Research Agent successfully searches via Brave API and returns structured results
- [ ] Email Agent creates Gmail drafts with proper OAuth2 authentication
- [ ] Research Agent can invoke Email Agent as a tool, passing research context
- [ ] CLI provides streaming responses with real-time tool execution visibility
- [ ] All unit tests pass with >80% code coverage
- [ ] Integration tests demonstrate end-to-end functionality
- [ ] Code meets quality standards (ruff, mypy, pytest)
- [ ] Documentation is comprehensive with setup instructions

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window

- url: https://ai.pydantic.dev/agents/
  why: Core agent creation patterns, tool registration, deps_type usage
  key_concepts: Agent initialization, @agent.tool decorator, RunContext

- url: https://ai.pydantic.dev/multi-agent-applications/
  why: Multi-agent system patterns, especially agent-as-tool implementation
  critical: Always pass ctx.usage when calling sub-agents for token tracking

- url: https://developers.google.com/gmail/api/guides/sending
  why: Gmail API authentication flow and draft creation
  section: OAuth2 setup, MIME message formatting, draft endpoints

- url: https://api.search.brave.com/app/documentation
  why: Brave Search API REST endpoints, parameters, rate limits
  critical: Rate limit is 2000 requests/month on free tier

- url: https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
  why: Official Gmail draft creation example with proper MIME encoding

- file: use-cases/agent-factory-with-subagents/examples/main_agent_reference/research_agent.py
  why: Reference pattern for multi-agent system with agent-as-tool
  key_pattern: How to invoke sub-agent with usage tracking

- file: use-cases/agent-factory-with-subagents/examples/main_agent_reference/tools.py
  why: Pure tool functions for Brave Search API integration
  key_pattern: Async tool implementation with error handling

- file: use-cases/agent-factory-with-subagents/examples/main_agent_reference/cli.py
  why: CLI structure with streaming responses and tool visibility
  key_pattern: Real-time streaming with rich console formatting

- file: use-cases/agent-factory-with-subagents/examples/main_agent_reference/settings.py
  why: Configuration management with pydantic-settings and python-dotenv
  key_pattern: Environment variable validation and loading

- file: use-cases/agent-factory-with-subagents/examples/main_agent_reference/.env.example
  why: Environment variable template structure
```

### Current Codebase tree
```bash
.
├── examples/
│   └── main_agent_reference/      # Reference implementation
│       ├── research_agent.py      # Multi-agent pattern reference
│       ├── tools.py               # Tool implementation patterns
│       ├── cli.py                 # CLI with streaming
│       ├── settings.py            # Configuration management
│       ├── providers.py           # LLM provider setup
│       └── .env.example           # Environment template
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md           # This template
│   └── EXAMPLE_multi_agent_prp.md # Example PRP
├── INITIAL.md                     # Feature requirements
├── CLAUDE.md                      # Project rules
└── venv_linux/                    # Virtual environment
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
.
├── agents/
│   ├── __init__.py                # Package initialization
│   ├── research_agent.py          # Primary agent with Brave Search and Email Agent integration
│   │                              # Responsibility: Coordinate research and email drafting
│   │                              # Tools: search_web, create_email_draft, summarize_research
│   ├── email_agent.py             # Sub-agent with Gmail draft creation capabilities
│   │                              # Responsibility: Create professional email drafts
│   │                              # Tools: create_gmail_draft
│   ├── dependencies.py            # Dependency dataclasses for both agents
│   │                              # Responsibility: Define dependency injection structure
│   ├── providers.py               # LLM provider configuration
│   │                              # Responsibility: Configure OpenAI/Anthropic/other providers
│   ├── models.py                  # Pydantic models for data validation
│   │                              # Responsibility: Define data structures and validation
│   ├── tools.py                   # Pure tool functions (Brave Search, Gmail API)
│   │                              # Responsibility: External API integrations
│   ├── prompts.py                 # System prompts for both agents
│   │                              # Responsibility: Define agent behavior and capabilities
│   └── settings.py                # Configuration management with pydantic-settings
│                                  # Responsibility: Load and validate environment variables
├── tests/
│   ├── __init__.py                # Test package initialization
│   ├── conftest.py                # Pytest configuration and fixtures
│   ├── test_research_agent.py     # Research agent unit tests
│   ├── test_email_agent.py        # Email agent unit tests
│   ├── test_tools.py              # Tool function tests
│   ├── test_integration.py        # End-to-end integration tests
│   ├── test_cli.py                # CLI interface tests
│   └── test_dependencies.py       # Dependency injection tests
├── cli.py                         # Interactive CLI with streaming and tool visibility
│                                  # Responsibility: User interface for agent interaction
├── .env.example                   # Environment variables template with descriptions
├── requirements.txt               # Python package dependencies
├── README.md                      # Comprehensive documentation with setup instructions
└── credentials/                   # Directory for Gmail credentials (gitignored)
    └── .gitkeep                   # Keep directory in git
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: Pydantic AI requires async throughout - no sync functions in async agent context
# REASON: Agent.run() and tool functions operate asynchronously

# CRITICAL: Gmail API requires OAuth2 flow on first run - credentials.json needed
# REASON: User must authorize application to access Gmail on behalf of user
# FIRST RUN: Browser opens for authorization, token.json is created and cached

# CRITICAL: Brave API has rate limits - 2000 req/month on free tier, 429 status on exceed
# REASON: Free tier has monthly quota, must handle rate limit errors gracefully

# CRITICAL: Agent-as-tool pattern requires passing ctx.usage for token tracking
# PATTERN: result = await sub_agent.run(prompt, deps=sub_deps, usage=ctx.usage)
# REASON: Ensures token usage is tracked across the entire multi-agent conversation

# CRITICAL: Gmail drafts need base64 encoding with proper MIME formatting
# REASON: Gmail API expects RFC 2822 format messages, base64url encoded
# PATTERN: Use email.mime.text.MIMEText + base64.urlsafe_b64encode

# CRITICAL: Always use python-dotenv with load_dotenv() in settings.py
# REASON: Loads .env file before pydantic-settings reads environment variables
# PATTERN: Call load_dotenv() at module level before Settings class definition

# CRITICAL: Store sensitive credentials in .env, never commit them
# REASON: Security - API keys and OAuth tokens should never be in version control
# PATTERN: Use .env.example with placeholder values, .gitignore .env file

# CRITICAL: Use pydantic-settings BaseSettings for configuration
# REASON: Provides validation, type safety, and automatic environment variable loading
# PATTERN: Follow examples/main_agent_reference/settings.py structure

# CRITICAL: Virtual environment (venv_linux) must be used for all commands
# REASON: Project rules in CLAUDE.md require consistent environment
# PATTERN: source venv_linux/bin/activate or use venv_linux/bin/python

# CRITICAL: Files should never exceed 500 lines of code
# REASON: Modularity rule from CLAUDE.md for maintainability
# PATTERN: Split large files into focused modules

# CRITICAL: All functions need Google-style docstrings
# REASON: Project documentation standard from CLAUDE.md
# PATTERN: Brief summary, Args section, Returns section

# CRITICAL: Use @agent.tool for context-aware tools, @agent.tool_plain for simple tools
# REASON: Tools needing RunContext[DepsType] use @agent.tool
# PATTERN: Search tool needs API key from deps, so use @agent.tool with RunContext
```

## Implementation Blueprint

### Data models and structure

Create core data models to ensure type safety and consistency across the multi-agent system.

```python
# models.py - Core data structures for the multi-agent system
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# === Research Agent Models ===

class BraveSearchResult(BaseModel):
    """Individual search result from Brave API."""
    title: str = Field(..., description="Result title")
    url: str = Field(..., description="Result URL")
    description: str = Field(..., description="Result description/snippet")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")

class ResearchQuery(BaseModel):
    """Research query parameters."""
    query: str = Field(..., min_length=1, description="Search query")
    max_results: int = Field(10, ge=1, le=20, description="Maximum results to return")
    include_summary: bool = Field(True, description="Include research summary")

class ResearchSummary(BaseModel):
    """Structured research summary."""
    topic: str = Field(..., description="Research topic")
    key_findings: List[str] = Field(default_factory=list, description="Key findings")
    sources: List[str] = Field(default_factory=list, description="Source URLs")
    summary_text: str = Field(..., description="Human-readable summary")
    timestamp: datetime = Field(default_factory=datetime.now)

# === Email Agent Models ===

class EmailDraft(BaseModel):
    """Email draft structure for Gmail."""
    recipient: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None

class GmailDraftResponse(BaseModel):
    """Response from Gmail API after draft creation."""
    draft_id: str = Field(..., description="Gmail draft ID")
    message_id: str = Field(..., description="Gmail message ID")
    thread_id: str = Field(..., description="Gmail thread ID")

# === Dependency Models ===

from dataclasses import dataclass

@dataclass
class ResearchAgentDependencies:
    """Dependencies for Research Agent execution."""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None

@dataclass
class EmailAgentDependencies:
    """Dependencies for Email Agent execution."""
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1: Setup Configuration and Environment Management
CREATE agents/settings.py:
  - PATTERN: Follow examples/main_agent_reference/settings.py structure
  - Use pydantic-settings BaseSettings for configuration
  - Call load_dotenv() at module level before Settings class
  - Validate required API keys with @field_validator
  - Include fields: llm_provider, llm_api_key, llm_model, llm_base_url
  - Include fields: brave_api_key, brave_search_url
  - Include fields: gmail_credentials_path, gmail_token_path
  - Include fields: app_env, log_level, debug

CREATE .env.example:
  - PATTERN: Follow examples/main_agent_reference/.env.example structure
  - Include LLM configuration section with comments
  - Include Brave Search API key with comment about rate limits
  - Include Gmail OAuth paths with setup instructions
  - Include application configuration (env, log level)
  - Add clear instructions about obtaining API keys

Task 2: Create Data Models and Structures
CREATE agents/models.py:
  - PATTERN: Use Pydantic BaseModel for all data structures
  - Define BraveSearchResult with title, url, description, score
  - Define ResearchQuery with validation (max_results 1-20)
  - Define EmailDraft with EmailStr validation
  - Define GmailDraftResponse with Gmail IDs
  - Define ResearchAgentDependencies dataclass
  - Define EmailAgentDependencies dataclass
  - Add comprehensive docstrings for each model

Task 3: Create System Prompts
CREATE agents/prompts.py:
  - Define RESEARCH_AGENT_PROMPT (200-400 words)
    * Describe capabilities: web search, email creation
    * Provide guidance on research synthesis
    * Explain when to create email drafts
  - Define EMAIL_AGENT_PROMPT (150-300 words)
    * Focus on professional email writing
    * Explain Gmail draft creation capability
    * Emphasize tone and structure
  - Keep prompts clear, focused, and actionable

Task 4: Implement LLM Provider Configuration
CREATE agents/providers.py:
  - PATTERN: Follow examples/main_agent_reference/providers.py
  - Import from pydantic_ai.providers (openai, anthropic, gemini)
  - Create get_llm_model() function
  - Support multiple providers based on settings.llm_provider
  - Handle provider-specific initialization
  - Return configured model instance
  - Add error handling for invalid providers

Task 5: Implement Brave Search Tool
CREATE agents/tools.py (Part 1 - Brave Search):
  - PATTERN: Follow examples/main_agent_reference/tools.py structure
  - Implement async search_web_tool() function
  - Use httpx.AsyncClient for async HTTP requests
  - Handle Brave API authentication with X-Subscription-Token header
  - Parse response and extract web.results array
  - Calculate relevance scores based on result position
  - Handle errors: 401 (invalid key), 429 (rate limit), network errors
  - Return List[Dict[str, Any]] with title, url, description, score
  - Add comprehensive logging and docstring

Task 6: Implement Gmail Tool
CREATE agents/tools.py (Part 2 - Gmail):
  - PATTERN: Study gmail API examples from Google documentation
  - Implement async create_gmail_draft_tool() function
  - Handle OAuth2 flow:
    * Load credentials from gmail_credentials_path
    * Check for existing token at gmail_token_path
    * If no token, initiate OAuth flow (opens browser)
    * Save token for future use
  - Create MIME message:
    * Use email.mime.text.MIMEText for message structure
    * Set To, Subject, From headers
    * Encode message as base64url (no padding)
  - Call Gmail API drafts.create endpoint
  - Return draft ID and message details
  - Handle authentication refresh automatically
  - Add comprehensive error handling and logging

Task 7: Create Email Draft Agent
CREATE agents/email_agent.py:
  - PATTERN: Follow agent creation from examples/main_agent_reference
  - Import Agent, RunContext from pydantic_ai
  - Import dependencies, prompts, models, providers
  - Create EmailAgentDependencies dataclass
  - Initialize email_agent with:
    * get_llm_model() for model
    * deps_type=EmailAgentDependencies
    * system_prompt=EMAIL_AGENT_PROMPT

  - Register tool: @email_agent.tool create_gmail_draft
    * Parameters: ctx, recipient, subject, body
    * Extract Gmail paths from ctx.deps
    * Call create_gmail_draft_tool() from tools.py
    * Return structured draft creation result
    * Handle errors and provide user-friendly messages

  - Add create_email_agent() convenience function
  - Add comprehensive logging

Task 8: Create Research Agent with Multi-Agent Integration
CREATE agents/research_agent.py:
  - PATTERN: Follow examples/main_agent_reference/research_agent.py
  - Import Agent, RunContext from pydantic_ai
  - Import email_agent, dependencies, models, prompts, providers, tools
  - Create ResearchAgentDependencies dataclass
  - Initialize research_agent with:
    * get_llm_model() for model
    * deps_type=ResearchAgentDependencies
    * system_prompt=RESEARCH_AGENT_PROMPT

  - Register tool: @research_agent.tool search_web
    * Parameters: ctx, query, max_results=10
    * Validate max_results range (1-20)
    * Extract brave_api_key from ctx.deps
    * Call search_web_tool() from tools.py
    * Return List[Dict] with search results
    * Handle errors gracefully

  - Register tool: @research_agent.tool create_email_draft
    * Parameters: ctx, recipient_email, subject, context, research_summary=None
    * Build email prompt with research context
    * Create EmailAgentDependencies from ctx.deps
    * CRITICAL: Call email_agent.run() with usage=ctx.usage
    * Return draft creation result with success status
    * Handle errors and provide feedback

  - Register tool: @research_agent.tool summarize_research
    * Parameters: ctx, search_results, topic, focus_areas=None
    * Extract key information from search results
    * Format sources and descriptions
    * Return structured summary

  - Add create_research_agent() convenience function
  - Add comprehensive logging throughout

Task 9: Implement Dependencies Module
CREATE agents/dependencies.py:
  - Import dataclasses, Optional
  - Define ResearchAgentDependencies dataclass:
    * brave_api_key: str
    * gmail_credentials_path: str
    * gmail_token_path: str
    * session_id: Optional[str] = None
  - Define EmailAgentDependencies dataclass:
    * gmail_credentials_path: str
    * gmail_token_path: str
    * session_id: Optional[str] = None
  - Add docstrings explaining dependency injection pattern

Task 10: Create Package Initialization
CREATE agents/__init__.py:
  - Import and expose main agent instances
  - Import and expose dependency classes
  - Import and expose model classes
  - Document package structure
  - Make agents easily importable: from agents import research_agent

Task 11: Implement CLI Interface with Streaming
CREATE cli.py:
  - PATTERN: Follow examples/main_agent_reference/cli.py structure
  - Import asyncio, rich (Console, Panel, Prompt, Live, Text)
  - Import research_agent, ResearchAgentDependencies, settings

  - Implement async stream_agent_interaction():
    * Set up dependencies from settings
    * Build context with conversation history (last 6 messages)
    * Use async with research_agent.iter() for streaming
    * Handle different node types:
      - user_prompt_node: Silent start
      - model_request_node: Stream text with PartDeltaEvent
      - call_tools_node: Display tool calls with FunctionToolCallEvent
      - end_node: Clean completion
    * Display tool execution in real-time with rich formatting
    * Return tuple (streamed_text, final_output)

  - Implement async main():
    * Display welcome panel with instructions
    * Initialize conversation_history list
    * Interactive loop:
      - Prompt user for input
      - Handle 'exit'/'quit' commands
      - Add to conversation history
      - Stream agent interaction
      - Display responses with proper formatting
    * Handle KeyboardInterrupt gracefully

  - Add if __name__ == "__main__": asyncio.run(main())
  - Use rich console for beautiful formatted output

Task 12: Create Comprehensive Test Suite
CREATE tests/conftest.py:
  - Import pytest, os, sys
  - Add fixtures:
    * mock_settings: Mocked Settings with test values
    * mock_brave_api: Mock Brave API responses
    * mock_gmail_api: Mock Gmail API responses
    * sample_search_results: Test data for search results
    * sample_email_draft: Test data for email drafts
  - Set up test environment variables

CREATE tests/test_tools.py:
  - PATTERN: Test happy path, edge cases, errors for each tool
  - Test search_web_tool():
    * Happy path: Returns valid results
    * Error: Invalid API key (401)
    * Error: Rate limit exceeded (429)
    * Edge: Empty query
    * Edge: max_results validation
  - Test create_gmail_draft_tool() (with mocks):
    * Happy path: Creates draft successfully
    * Error: Invalid credentials
    * Error: Token refresh needed
    * Edge: Missing parameters

CREATE tests/test_research_agent.py:
  - PATTERN: Use TestModel or FunctionModel for testing
  - Test research agent initialization
  - Test search_web tool registration
  - Test create_email_draft tool registration
  - Test summarize_research tool
  - Mock external API calls
  - Verify agent responds to queries
  - Test error handling

CREATE tests/test_email_agent.py:
  - Test email agent initialization
  - Test create_gmail_draft tool registration
  - Mock Gmail API calls
  - Verify draft creation logic
  - Test email validation
  - Test error handling

CREATE tests/test_integration.py:
  - Test end-to-end flow:
    * User query → Research → Results
    * User request → Research → Email draft
  - Use TestModel to avoid API calls
  - Verify multi-agent communication
  - Test ctx.usage passing
  - Test conversation history

CREATE tests/test_cli.py:
  - Test CLI initialization
  - Test user input handling
  - Test streaming display (mock agent responses)
  - Test exit commands
  - Test error handling in CLI

CREATE tests/test_dependencies.py:
  - Test dependency dataclasses
  - Test dependency injection
  - Test settings validation

Task 13: Create Documentation
CREATE README.md:
  - PATTERN: Follow examples with clear structure
  - Include sections:
    * Project overview
    * Features list
    * Architecture diagram (text-based)
    * Installation instructions
    * API key configuration (Brave, Gmail OAuth setup)
    * Usage examples with CLI commands
    * Testing instructions
    * Troubleshooting common issues
    * Project structure explanation
  - Make setup instructions copy-paste friendly
  - Include security best practices

Task 14: Create Requirements File
CREATE requirements.txt:
  - Include core dependencies:
    * pydantic-ai[anthropic,openai,gemini]
    * pydantic-settings
    * python-dotenv
    * httpx
    * google-api-python-client
    * google-auth-httplib2
    * google-auth-oauthlib
    * rich
    * pytest
    * pytest-asyncio
    * pytest-mock
    * pytest-cov
  - Pin versions for stability
  - Add comments for clarity

Task 15: Create Credentials Directory
CREATE credentials/.gitkeep:
  - Keep empty directory in git for Gmail credentials

UPDATE .gitignore:
  - Add credentials/*.json
  - Add credentials/token.json
  - Add .env
  - Add __pycache__/
  - Add *.pyc
  - Add .pytest_cache/
  - Add venv*/
```

### Per task pseudocode as needed added to each task

```python
# Task 5: Brave Search Tool - CRITICAL implementation details
async def search_web_tool(
    api_key: str,
    query: str,
    count: int = 10,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Pure async function to search Brave API.

    CRITICAL: This is a standalone function, NOT an agent tool decorator.
    PATTERN: Will be called by @research_agent.tool wrapper that has RunContext.
    """
    # GOTCHA: Validate inputs before API call to avoid wasting quota
    if not api_key or not api_key.strip():
        raise ValueError("Brave API key is required")

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    # GOTCHA: Brave API only accepts count 1-20
    count = min(max(count, 1), 20)

    headers = {
        "X-Subscription-Token": api_key,  # CRITICAL: Header name for Brave
        "Accept": "application/json"
    }

    params = {"q": query, "count": count, "offset": offset}

    # PATTERN: Use httpx AsyncClient for async HTTP
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=30.0  # CRITICAL: Prevent hanging
            )

            # GOTCHA: Brave returns 429 on rate limit (2000/month free tier)
            if response.status_code == 429:
                raise Exception("Brave API rate limit exceeded. Check quota.")

            # GOTCHA: Returns 401 for invalid key
            if response.status_code == 401:
                raise Exception("Invalid Brave API key")

            if response.status_code != 200:
                raise Exception(f"API error {response.status_code}: {response.text}")

            data = response.json()

            # PATTERN: Brave response structure: {"web": {"results": [...]}}
            web_results = data.get("web", {}).get("results", [])

            # PATTERN: Convert to our standardized format
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
            # PATTERN: Convert HTTP errors to user-friendly messages
            raise Exception(f"Request failed: {str(e)}")


# Task 6: Gmail Tool - CRITICAL OAuth2 and MIME handling
async def create_gmail_draft_tool(
    credentials_path: str,
    token_path: str,
    recipient: str,
    subject: str,
    body: str
) -> Dict[str, Any]:
    """
    Create Gmail draft with OAuth2 authentication.

    CRITICAL: Gmail API requires OAuth2 flow on first use.
    PATTERN: Uses google-auth-oauthlib for authentication.
    """
    import base64
    from email.mime.text import MIMEText
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    # CRITICAL: Gmail API scope for draft creation
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

    creds = None

    # PATTERN: Check for existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # GOTCHA: Token might be expired, refresh if needed
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # CRITICAL: If no valid credentials, run OAuth flow (opens browser)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES
        )
        # GOTCHA: This opens a browser for user authorization
        creds = flow.run_local_server(port=0)

        # PATTERN: Save token for future runs
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # CRITICAL: Create MIME message (RFC 2822 format)
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject

    # CRITICAL: Gmail API requires base64url encoding (no padding)
    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode('utf-8')

    # PATTERN: Create draft via Gmail API
    draft = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw_message}}
    ).execute()

    # PATTERN: Return structured response
    return {
        "draft_id": draft['id'],
        "message_id": draft['message']['id'],
        "thread_id": draft['message'].get('threadId', '')
    }


# Task 8: Research Agent Multi-Agent Integration - CRITICAL usage passing
from pydantic_ai import Agent, RunContext
from .email_agent import email_agent, EmailAgentDependencies

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

    CRITICAL: Must pass ctx.usage for token tracking across agents.
    PATTERN: Build detailed prompt, create sub-agent deps, invoke with usage.
    """
    # PATTERN: Build comprehensive prompt for email agent
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

    # PATTERN: Create dependencies for email agent from parent deps
    email_deps = EmailAgentDependencies(
        gmail_credentials_path=ctx.deps.gmail_credentials_path,
        gmail_token_path=ctx.deps.gmail_token_path,
        session_id=ctx.deps.session_id
    )

    # CRITICAL: Pass usage=ctx.usage for token tracking
    # REASON: Pydantic AI needs to track tokens across entire multi-agent conversation
    result = await email_agent.run(
        email_prompt,
        deps=email_deps,
        usage=ctx.usage  # CRITICAL: Token tracking
    )

    return {
        "success": True,
        "agent_response": result.data,
        "recipient": recipient_email,
        "subject": subject,
        "context": context
    }


# Task 11: CLI Streaming - CRITICAL event handling
async def stream_agent_interaction(
    user_input: str,
    conversation_history: List[str]
) -> tuple[str, str]:
    """
    Stream agent responses with real-time tool visibility.

    PATTERN: Use async with agent.iter() for streaming.
    CRITICAL: Handle different node types for proper display.
    """
    # Set up dependencies from settings
    research_deps = ResearchAgentDependencies(
        brave_api_key=settings.brave_api_key,
        gmail_credentials_path=settings.gmail_credentials_path,
        gmail_token_path=settings.gmail_token_path
    )

    # PATTERN: Build context with history (keep last 6 messages)
    context = "\n".join(conversation_history[-6:]) if conversation_history else ""

    prompt = f"""Previous conversation:
{context}

User: {user_input}

Respond naturally and helpfully."""

    response_text = ""

    # CRITICAL: Use async with agent.iter() for streaming
    async with research_agent.iter(prompt, deps=research_deps) as run:

        async for node in run:

            # PATTERN: Check node type with Agent.is_* methods
            if Agent.is_user_prompt_node(node):
                pass  # Silent start

            # CRITICAL: model_request_node for streaming text
            elif Agent.is_model_request_node(node):
                console.print("[bold blue]Assistant:[/bold blue] ", end="")

                # PATTERN: Stream events from node.stream()
                async with node.stream(run.ctx) as request_stream:
                    async for event in request_stream:
                        event_type = type(event).__name__

                        # GOTCHA: Check event type by name
                        if event_type == "PartDeltaEvent":
                            if hasattr(event, 'delta') and hasattr(event.delta, 'content_delta'):
                                delta_text = event.delta.content_delta
                                if delta_text:
                                    console.print(delta_text, end="")
                                    response_text += delta_text

                        elif event_type == "FinalResultEvent":
                            console.print()  # New line

            # CRITICAL: call_tools_node for tool execution visibility
            elif Agent.is_call_tools_node(node):
                async with node.stream(run.ctx) as tool_stream:
                    async for event in tool_stream:
                        event_type = type(event).__name__

                        if event_type == "FunctionToolCallEvent":
                            # PATTERN: Extract tool name from event.part
                            tool_name = "Unknown"
                            args = None

                            if hasattr(event, 'part'):
                                if hasattr(event.part, 'tool_name'):
                                    tool_name = event.part.tool_name
                                if hasattr(event.part, 'args'):
                                    args = event.part.args

                            # PATTERN: Display tool call with rich formatting
                            console.print(f"  🔹 [cyan]Calling tool:[/cyan] [bold]{tool_name}[/bold]")

                            if args and isinstance(args, dict):
                                arg_preview = []
                                for key, value in list(args.items())[:3]:
                                    val_str = str(value)
                                    if len(val_str) > 50:
                                        val_str = val_str[:47] + "..."
                                    arg_preview.append(f"{key}={val_str}")
                                console.print(f"    [dim]Args: {', '.join(arg_preview)}[/dim]")

                        elif event_type == "FunctionToolResultEvent":
                            result = str(event.tool_return) if hasattr(event, 'tool_return') else "No result"
                            if len(result) > 100:
                                result = result[:97] + "..."
                            console.print(f"  ✅ [green]Tool result:[/green] [dim]{result}[/dim]")

            elif Agent.is_end_node(node):
                pass  # Clean completion

    # PATTERN: Get final result
    final_result = run.result
    final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)

    return (response_text.strip(), final_output)
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env (created from .env.example)
  - vars: |
      # LLM Configuration
      LLM_PROVIDER=openai
      LLM_API_KEY=sk-...
      LLM_MODEL=gpt-4o-mini
      LLM_BASE_URL=https://api.openai.com/v1

      # Brave Search API
      BRAVE_API_KEY=BSA...  # Get from https://brave.com/search/api/

      # Gmail OAuth2 Configuration
      GMAIL_CREDENTIALS_PATH=./credentials/credentials.json
      GMAIL_TOKEN_PATH=./credentials/token.json

      # Application Configuration
      APP_ENV=development
      LOG_LEVEL=INFO
      DEBUG=false

CONFIG:
  - Gmail OAuth:
    * First run opens browser for authorization
    * User grants access to Gmail drafts
    * Token saved to GMAIL_TOKEN_PATH for future runs
  - Token storage:
    * ./credentials/token.json (auto-created after OAuth)
    * Token automatically refreshed when expired
  - Security:
    * Never commit credentials.json or token.json
    * Add credentials/ directory to .gitignore
    * Use .env.example with placeholder values

DEPENDENCIES:
  - Virtual environment: venv_linux (must be activated)
  - Update requirements.txt with:
    * pydantic-ai[anthropic,openai,gemini]>=0.0.14
    * pydantic-settings>=2.0.0
    * python-dotenv>=1.0.0
    * httpx>=0.27.0
    * google-api-python-client>=2.100.0
    * google-auth-httplib2>=0.2.0
    * google-auth-oauthlib>=1.2.0
    * rich>=13.0.0
    * pytest>=8.0.0
    * pytest-asyncio>=0.23.0
    * pytest-mock>=3.12.0
    * pytest-cov>=4.1.0

GMAIL_OAUTH_SETUP:
  - Step 1: Get credentials.json from Google Cloud Console
    * Go to https://console.cloud.google.com
    * Create new project or select existing
    * Enable Gmail API
    * Create OAuth 2.0 Client ID (Desktop app)
    * Download credentials.json
  - Step 2: Place credentials.json in credentials/ directory
  - Step 3: First run of CLI will open browser for authorization
  - Step 4: Authorize application, token.json created automatically
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# CRITICAL: Run in venv_linux virtual environment
source venv_linux/bin/activate  # Or use venv_linux/bin/python

# Run these FIRST - fix any errors before proceeding
ruff check agents/ cli.py --fix    # Auto-fix style issues
ruff check tests/ --fix            # Fix test style issues
mypy agents/                       # Type checking (ignore test typing for now)

# Expected: No errors. If errors, READ the error and fix before continuing.
# Common errors:
# - Missing imports
# - Type annotation issues
# - Async/await usage
```

### Level 2: Unit Tests
```python
# PATTERN: Each test file focuses on specific component
# Use TestModel or FunctionModel to avoid API calls in tests

# tests/test_tools.py - Example patterns
import pytest
from unittest.mock import patch, AsyncMock
from agents.tools import search_web_tool, create_gmail_draft_tool

@pytest.mark.asyncio
async def test_search_web_happy_path():
    """Test Brave search returns valid results."""
    # PATTERN: Mock httpx response
    mock_response = {
        "web": {
            "results": [
                {"title": "Test", "url": "https://test.com", "description": "Test result"}
            ]
        }
    }

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: mock_response
        )

        results = await search_web_tool(
            api_key="test_key",
            query="test query",
            count=10
        )

        assert len(results) == 1
        assert results[0]["title"] == "Test"
        assert results[0]["score"] > 0

@pytest.mark.asyncio
async def test_search_web_rate_limit():
    """Test handling of Brave API rate limit."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(status_code=429)

        with pytest.raises(Exception) as exc_info:
            await search_web_tool(api_key="test_key", query="test")

        assert "rate limit" in str(exc_info.value).lower()

@pytest.mark.asyncio
async def test_search_web_invalid_key():
    """Test handling of invalid Brave API key."""
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(status_code=401)

        with pytest.raises(Exception) as exc_info:
            await search_web_tool(api_key="invalid", query="test")

        assert "invalid" in str(exc_info.value).lower()

def test_search_web_empty_query():
    """Test validation of empty query."""
    import asyncio
    with pytest.raises(ValueError) as exc_info:
        asyncio.run(search_web_tool(api_key="key", query=""))

    assert "empty" in str(exc_info.value).lower()


# tests/test_research_agent.py - Example patterns
import pytest
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
from agents.research_agent import research_agent, ResearchAgentDependencies

@pytest.mark.asyncio
async def test_research_agent_initialization():
    """Test research agent initializes correctly."""
    assert research_agent is not None
    assert research_agent.deps_type == ResearchAgentDependencies

@pytest.mark.asyncio
async def test_research_with_test_model():
    """Test research agent with TestModel (no API calls)."""
    # PATTERN: Use TestModel for testing without API costs
    test_agent = research_agent.override(model=TestModel())

    deps = ResearchAgentDependencies(
        brave_api_key="test_key",
        gmail_credentials_path="test.json",
        gmail_token_path="token.json"
    )

    # PATTERN: TestModel returns simple responses
    result = await test_agent.run(
        "Tell me about AI",
        deps=deps
    )

    assert result.data is not None


# tests/test_integration.py - End-to-end patterns
@pytest.mark.asyncio
async def test_research_to_email_flow():
    """Test complete flow: research query -> email draft."""
    # PATTERN: Use TestModel for both agents
    from pydantic_ai.models.test import TestModel
    from agents.research_agent import research_agent
    from agents.email_agent import email_agent

    test_research = research_agent.override(model=TestModel())
    test_email = email_agent.override(model=TestModel())

    # Simulate research followed by email creation
    research_deps = ResearchAgentDependencies(
        brave_api_key="test",
        gmail_credentials_path="test.json",
        gmail_token_path="token.json"
    )

    result = await test_research.run(
        "Research AI and create email to test@example.com",
        deps=research_deps
    )

    assert result.data is not None
    # PATTERN: Verify multi-agent communication worked
```

```bash
# Run all tests with coverage
source venv_linux/bin/activate
pytest tests/ -v --cov=agents --cov=cli --cov-report=term-missing --cov-report=html

# Expected: >80% coverage, all tests passing
# If failing:
# 1. Read the error carefully
# 2. Check if it's a test issue or code issue
# 3. Fix the root cause
# 4. Re-run tests
# 5. NEVER mock just to pass tests - fix the actual issue

# Run specific test file for debugging
pytest tests/test_research_agent.py -v -s

# Run specific test function
pytest tests/test_tools.py::test_search_web_happy_path -v -s
```

### Level 3: Integration Test (Manual CLI Testing)
```bash
# CRITICAL: Set up environment first
source venv_linux/bin/activate
cp .env.example .env
# Edit .env with real API keys:
# - Add your OpenAI/Anthropic API key
# - Add your Brave Search API key
# - Set Gmail credentials path (if testing email functionality)

# Start the CLI
python cli.py

# Expected interaction flow:
# ========================

# Welcome message displayed
# 🤖 Pydantic AI Research Assistant
# Real-time tool execution visibility
# Type 'exit' to quit

# Test 1: Basic research query
You: Research latest developments in AI safety

# Expected output:
# Assistant: [streaming text response]
#   🔹 Calling tool: search_web
#     Args: query=AI safety developments, max_results=10
#   ✅ Tool result: [List of search results...]
# [Agent synthesizes results and provides summary]

# Test 2: Research with email creation
You: Research AI safety and draft an email about it to john@example.com

# Expected output:
# Assistant: [streaming text about research]
#   🔹 Calling tool: search_web
#     Args: query=AI safety, max_results=10
#   ✅ Tool result: [Search results]
#   🔹 Calling tool: create_email_draft
#     Args: recipient_email=john@example.com, subject=..., context=...
#   ✅ Tool result: {"success": true, "draft_id": "..."}
# [Agent confirms email draft created]

# Test 3: Gmail OAuth flow (first time only)
# If Gmail credentials configured:
# - Browser opens automatically
# - User authorizes application
# - Token saved to credentials/token.json
# - Draft created in Gmail drafts folder

# Test 4: Error handling
You: Search for something with invalid query!!!@@@

# Expected: Agent handles gracefully, explains issue

# Test 5: Exit
You: exit

# Expected: 👋 Goodbye!

# Validation checks:
# ✅ CLI starts without errors
# ✅ Streaming works (text appears in real-time)
# ✅ Tool calls are visible with arguments
# ✅ Search results are returned and formatted
# ✅ Email drafts are created (check Gmail drafts folder)
# ✅ Conversation history is maintained
# ✅ Error messages are user-friendly
# ✅ Exit command works cleanly
```

## Final Validation Checklist
```yaml
Code Quality:
  - [ ] All tests pass: pytest tests/ -v
  - [ ] Coverage >80%: pytest --cov=agents --cov=cli --cov-report=term
  - [ ] No linting errors: ruff check agents/ cli.py
  - [ ] No type errors: mypy agents/
  - [ ] Files under 500 lines: wc -l agents/*.py cli.py
  - [ ] All functions have Google-style docstrings
  - [ ] No hardcoded secrets or API keys

Functionality:
  - [ ] Research Agent searches via Brave API successfully
  - [ ] Search results are structured and relevant
  - [ ] Email Agent creates Gmail drafts with proper authentication
  - [ ] Research Agent invokes Email Agent as tool (multi-agent pattern works)
  - [ ] Token usage is tracked across agents (ctx.usage passed correctly)
  - [ ] Error cases handled gracefully (rate limits, auth failures, network errors)

User Experience:
  - [ ] CLI provides real-time streaming responses
  - [ ] Tool execution is visible with arguments and results
  - [ ] Tool calls are formatted beautifully with rich console
  - [ ] Conversation history is maintained
  - [ ] Error messages are user-friendly
  - [ ] Exit commands work cleanly

Documentation:
  - [ ] README includes clear setup instructions
  - [ ] README includes API key configuration steps
  - [ ] README includes Gmail OAuth setup guide
  - [ ] README includes usage examples
  - [ ] README includes troubleshooting section
  - [ ] .env.example has all required variables with comments
  - [ ] Code comments explain non-obvious logic
  - [ ] Project structure is documented

Security & Best Practices:
  - [ ] .env file in .gitignore
  - [ ] credentials/ directory in .gitignore
  - [ ] API keys loaded from environment variables
  - [ ] OAuth tokens stored securely
  - [ ] No sensitive data in version control
  - [ ] Dependencies pinned in requirements.txt
  - [ ] Virtual environment (venv_linux) used for all operations

Integration:
  - [ ] Gmail OAuth flow works (browser opens, token saved)
  - [ ] Brave Search returns results (respects rate limits)
  - [ ] Multi-agent communication works (research → email)
  - [ ] CLI handles user input correctly
  - [ ] Streaming works in real-time
  - [ ] All external API integrations tested
```

---

## Anti-Patterns to Avoid
```python
# ❌ Don't hardcode API keys or secrets
brave_api_key = "BSA123..."  # WRONG
# ✅ Do load from environment
brave_api_key = settings.brave_api_key  # CORRECT

# ❌ Don't use sync functions in async agent context
def search_web(query: str):  # WRONG - blocking
    return requests.get(url)
# ✅ Do use async functions
async def search_web_tool(query: str):  # CORRECT
    async with httpx.AsyncClient() as client:
        return await client.get(url)

# ❌ Don't skip OAuth flow setup for Gmail
# Just assuming credentials exist - WRONG
# ✅ Do implement proper OAuth flow
if not os.path.exists(token_path):
    flow = InstalledAppFlow.from_client_secrets_file(...)
    creds = flow.run_local_server(port=0)

# ❌ Don't ignore rate limits for APIs
# Keep calling without checking - WRONG
# ✅ Do handle rate limit errors
if response.status_code == 429:
    raise Exception("Rate limit exceeded. Check quota.")

# ❌ Don't forget to pass ctx.usage in multi-agent calls
result = await email_agent.run(prompt, deps=deps)  # WRONG - no token tracking
# ✅ Do pass usage for token tracking
result = await email_agent.run(prompt, deps=deps, usage=ctx.usage)  # CORRECT

# ❌ Don't commit credentials.json or token.json files
git add credentials/credentials.json  # WRONG
# ✅ Do add to .gitignore
# In .gitignore:
credentials/*.json
credentials/token.json

# ❌ Don't create files longer than 500 lines
# One huge agent.py with everything - WRONG
# ✅ Do split into focused modules
agents/
  research_agent.py  # ~200 lines
  email_agent.py     # ~150 lines
  tools.py           # ~200 lines
  models.py          # ~100 lines

# ❌ Don't skip error handling
result = await external_api.call()  # WRONG - no try/except
# ✅ Do handle errors gracefully
try:
    result = await external_api.call()
except httpx.RequestError as e:
    logger.error(f"API call failed: {e}")
    return {"error": f"Failed to call API: {str(e)}"}

# ❌ Don't use sync Python dotenv loading
settings = Settings()  # WRONG - .env not loaded yet
# ✅ Do call load_dotenv() before Settings
from dotenv import load_dotenv
load_dotenv()  # Load .env file
settings = Settings()  # Now reads environment variables

# ❌ Don't mock tests just to pass
@patch('everything')
def test_agent(mock_all):  # WRONG - not testing real behavior
    mock_all.return_value = True
    assert True
# ✅ Do test real behavior with TestModel
async def test_agent():  # CORRECT - tests actual agent logic
    test_agent = agent.override(model=TestModel())
    result = await test_agent.run("query", deps=deps)
    assert result.data is not None
```

---

## Confidence Score: 9/10

**High confidence due to:**
- Clear reference implementations in examples/main_agent_reference/
- Well-documented Pydantic AI patterns for multi-agent systems
- Established patterns for Brave Search and Gmail API integration
- Comprehensive validation gates with executable tests
- Detailed pseudocode for critical implementation sections
- Clear error handling and edge case documentation

**Minor uncertainty (1 point deduction):**
- Gmail OAuth first-time setup UX may require user assistance
- Brave API rate limits may impact testing on free tier
- First-time users may need guidance on obtaining Gmail credentials.json

**Mitigation strategies included:**
- Comprehensive README with Gmail OAuth setup guide
- Error messages guide users to documentation
- .env.example includes links to API key registration
- Troubleshooting section covers common issues

---

## Additional Notes

### Execution Strategy
1. **Follow task order strictly** - Dependencies flow from configuration → models → tools → agents → CLI
2. **Test incrementally** - After each task, run relevant tests before proceeding
3. **Use venv_linux** - All Python commands must use the virtual environment
4. **Commit frequently** - After each major task completion (optional but recommended)

### Common Pitfalls
1. **Forgetting load_dotenv()** - Must be called before Settings() initialization
2. **Missing ctx.usage** - Always pass usage when calling sub-agents
3. **Sync in async** - All tool functions must be async
4. **Ignoring 500-line limit** - Split files proactively before reaching limit

### Success Indicators
- Tests pass on first run (if implementation follows patterns exactly)
- CLI streams responses smoothly with visible tool calls
- Gmail drafts appear in user's Gmail drafts folder
- Brave search returns relevant results
- Error messages are helpful and actionable

### Time Estimate
- **Setup & Configuration**: 30 minutes
- **Core Implementation**: 2-3 hours
- **Testing & Validation**: 1-2 hours
- **Documentation**: 30 minutes
- **Total**: 4-6 hours for complete implementation

### Next Steps After Completion
1. Test with real API keys (Brave, OpenAI/Anthropic, Gmail)
2. Run full test suite and verify >80% coverage
3. Test CLI interface with various queries
4. Verify Gmail draft creation end-to-end
5. Document any issues or improvements needed
