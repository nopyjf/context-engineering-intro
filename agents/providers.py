"""
LLM Provider configuration supporting multiple providers.

This module provides flexible LLM model configuration supporting:
- OpenAI (and OpenAI-compatible APIs)
- Anthropic Claude
- Google Gemini
"""

from typing import Union
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.gemini import GeminiProvider
from .settings import settings


def get_llm_model() -> Model:
    """
    Get LLM model configuration based on environment variables.

    Supports multiple providers:
    - openai: OpenAI models (gpt-4, gpt-4o-mini, etc.)
    - anthropic: Anthropic Claude models
    - gemini: Google Gemini models

    Returns:
        Configured model instance based on settings

    Raises:
        ValueError: If provider is not supported
    """
    provider = settings.llm_provider.lower()
    api_key = settings.llm_api_key
    model_name = settings.llm_model

    if provider == "openai":
        # OpenAI or OpenAI-compatible provider
        provider_instance = OpenAIProvider(
            base_url=settings.llm_base_url,
            api_key=api_key
        )
        return OpenAIModel(model_name, provider=provider_instance)

    elif provider == "anthropic":
        # Anthropic Claude provider
        provider_instance = AnthropicProvider(api_key=api_key)
        return AnthropicModel(model_name, provider=provider_instance)

    elif provider == "gemini":
        # Google Gemini provider
        provider_instance = GeminiProvider(api_key=api_key)
        return GeminiModel(model_name, provider=provider_instance)

    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported providers: openai, anthropic, gemini"
        )


def get_model_info() -> dict:
    """
    Get information about current model configuration.

    Returns:
        Dictionary with model configuration info including:
        - llm_provider: Provider name
        - llm_model: Model name
        - llm_base_url: Base URL (for OpenAI-compatible providers)
        - app_env: Application environment
        - debug: Debug mode status
    """
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "app_env": settings.app_env,
        "debug": settings.debug,
    }


def validate_llm_configuration() -> bool:
    """
    Validate that LLM configuration is properly set.

    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        # Check if we can create a model instance
        model = get_llm_model()
        return model is not None
    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False
