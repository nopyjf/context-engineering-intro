# Multi-Agent Research & Email System

A production-ready multi-agent system built with Pydantic AI, featuring web research capabilities via Brave Search API and Gmail draft creation via Gmail API.

## Features

- **🔍 Web Research**: Search the web using Brave Search API for up-to-date information
- **📧 Email Drafting**: Create professional Gmail drafts based on research findings
- **🤖 Multi-Agent Architecture**: Research Agent delegates email composition to specialized Email Agent
- **⚡ Real-Time Streaming**: See agent thinking and tool execution in real-time
- **🔌 Multiple LLM Providers**: Support for OpenAI, Anthropic Claude, and Google Gemini
- **🧪 Comprehensive Testing**: Full test suite with >80% code coverage
- **🔒 Secure**: OAuth2 authentication for Gmail, environment-based API key management

## Installation

```bash
# Clone and navigate to project
cd Context-Engineering-Intro

# Create and activate virtual environment
python -m venv venv_linux
source venv_linux/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Edit `.env` with your configuration:

```bash
LLM_PROVIDER=openai
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini
BRAVE_API_KEY=your_brave_key_here
```

## Usage

```bash
python cli.py
```

## Testing

```bash
pytest tests/ -v --cov=agents --cov=cli
```

## Project Structure

```
agents/
├── research_agent.py    # Main research agent
├── email_agent.py       # Email draft agent
├── tools.py             # Brave & Gmail tools
├── models.py            # Data models
├── dependencies.py      # Dependency injection
├── providers.py         # LLM provider config
├── prompts.py           # System prompts
└── settings.py          # Configuration
cli.py                   # Interactive CLI
tests/                   # Comprehensive test suite
```

## License

MIT License - see LICENSE file for details.
