"""
LLM Provider Factory

Handles instantiation of LLM providers based on configuration.
Add new providers here to make them available via environment variables.
"""

import os
from .bedrock import BedrockProvider
from .openrouter import OpenRouterProvider

# Registry of available providers
PROVIDERS = {
    'bedrock': {
        'class': BedrockProvider,
        'config': lambda: {
            'region': os.getenv('AWS_REGION', 'us-east-1'),
            'model_id': os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0'),
            'api_key': os.getenv('BEDROCK_API_KEY')
        }
    },
    'openrouter': {
        'class': OpenRouterProvider,
        'config': lambda: {
            'api_key': os.getenv('OPENROUTER_API_KEY'),
            'model': os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-sonnet')
        }
    },
    # Add new providers here:
    # 'your_provider': {
    #     'class': YourProvider,
    #     'config': lambda: {
    #         'api_key': os.getenv('YOUR_PROVIDER_API_KEY'),
    #         # ... other config
    #     }
    # }
}

def create_llm_provider(provider_type: str = None):
    """
    Create LLM provider instance based on configuration
    
    Args:
        provider_type: Provider type (bedrock, openrouter, etc.)
                      If None, reads from LLM_PROVIDER env var
    
    Returns:
        Configured LLM provider instance
        
    Raises:
        ValueError: If provider type is unsupported or configuration is invalid
    """
    provider_type = provider_type or os.getenv('LLM_PROVIDER', 'bedrock').lower()
    
    if provider_type not in PROVIDERS:
        available = ', '.join(PROVIDERS.keys())
        raise ValueError(
            f"Unsupported LLM provider: '{provider_type}'. "
            f"Available providers: {available}"
        )
    
    provider_info = PROVIDERS[provider_type]
    config = provider_info['config']()
    
    # Validate required configuration
    if not all(config.values()):
        missing = [k for k, v in config.items() if not v]
        raise ValueError(
            f"Missing configuration for {provider_type}: {', '.join(missing)}"
        )
    
    return provider_info['class'](**config)

def list_providers():
    """List all available provider types"""
    return list(PROVIDERS.keys())
