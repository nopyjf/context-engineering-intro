## Multi-Agent Research & Email System

A production-ready multi-agent system built with Pydantic AI, featuring web research capabilities via Brave Search API and Gmail draft creation via Gmail API.

## Features

- **🔍 Web Research**: Search the web using Brave Search API for up-to-date information
- **📧 Email Drafting**: Create professional Gmail drafts based on research findings
- **🤖 Multi-Agent Architecture**: Research Agent delegates email composition to specialized Email Agent
- **⚡ Real-Time Streaming**: See agent thinking and tool execution in real-time
- **🔌 Multiple LLM Providers**: Support for OpenAI, Anthropic Claude, and Google Gemini
- **🧪 Comprehensive Testing**: Full test suite with >80% code coverage
- **🔒 Secure**: OAuth2 authentication for Gmail, environment-based API key management

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Interface                         │
│              (Real-time streaming & tool visibility)         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Research Agent                            │
│  • search_web: Brave Search API integration                  │
│  • summarize_research: Synthesize findings                   │
│  • create_email_draft: Delegate to Email Agent               │
└────────────┬───────────────────────────────┬────────────────┘
             │                               │
   ┌─────────▼─────────┐          ┌─────────▼──────────┐
   │  Brave Search API │          │   Email Agent       │
   │  (Web Search)     │          │  • create_gmail_draft│
   └───────────────────┘          └─────────┬───────────┘
                                             │
                                   ┌─────────▼─────────┐
                                   │    Gmail API      │
                                   │  (Draft Creation) │
                                   └───────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Virtual environment (venv_linux for this project)
- API keys for:
  - LLM provider (OpenAI, Anthropic, or Gemini)
  - Brave Search API
  - Gmail OAuth2 credentials (optional, for email features)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Context-Engineering-Intro
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv_linux
   source venv_linux/bin/activate  # On Windows: venv_linux\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Set up Gmail OAuth (Optional, for email features)**

   a. Go to [Google Cloud Console](https://console.cloud.google.com)

   b. Create a new project or select existing

   c. Enable Gmail API

   d. Create OAuth 2.0 Client ID:
      - Application type: Desktop app
      - Download credentials.json

   e. Place credentials.json in `./credentials/` directory

   f. On first run, browser will open for authorization

   g. After authorization, token.json is created automatically

## Configuration

### Required Environment Variables

Edit `.env` with your configuration:

```bash
# LLM Configuration
LLM_PROVIDER=openai  # Options: openai, anthropic, gemini
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1

# Brave Search API
BRAVE_API_KEY=your_brave_key_here

# Gmail OAuth2 (Optional)
GMAIL_CREDENTIALS_PATH=./credentials/credentials.json
GMAIL_TOKEN_PATH=./credentials/token.json

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
DEBUG=false
```

### Obtaining API Keys

**Brave Search API:**
1. Visit [Brave Search API](https://brave.com/search/api/)
2. Sign up for free tier (2000 requests/month)
3. Copy your API key

**OpenAI:**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy and store securely

**Anthropic:**
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Generate API key
3. Copy and store securely

**Google Gemini:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Copy and store securely

## Usage

### Running the CLI

```bash
# Activate virtual environment
source venv_linux/bin/activate

# Run the CLI
python cli.py
```

### Example Interactions

**Basic Research:**
```
You: Research the latest developments in quantum computing