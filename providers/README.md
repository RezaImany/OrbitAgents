# LLM Providers

This directory contains LLM provider implementations. Each provider is a self-contained class that handles communication with a specific LLM backend.

## Available Providers

- **BedrockProvider** - AWS Bedrock
- **OpenRouterProvider** - OpenRouter API

## Creating a New Provider

1. Create a new file: `providers/your_provider.py`
2. Inherit from `LLMProvider` base class
3. Implement required methods:
   - `ask(prompt, system_prompt, tools)` - Send request to LLM
   - `handle_tool_call(tool_use, mcp_client)` - Execute tool calls

### Example Template

```python
from .base import LLMProvider
from typing import List, Dict, Any, Optional

class YourProvider(LLMProvider):
    """Your LLM provider description"""
    
    def __init__(self, api_key: str, **kwargs):
        """
        Initialize provider
        
        Args:
            api_key: API key for authentication
            **kwargs: Provider-specific configuration
        """
        self.api_key = api_key
        # Add your initialization
    
    def ask(self, prompt: str, system_prompt: Optional[str] = None, 
            tools: Optional[List[Dict]] = None) -> Any:
        """
        Send request to LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            tools: Available tools (optional)
            
        Returns:
            LLM response
        """
        # Your implementation
        pass
    
    def handle_tool_call(self, tool_use: Dict, mcp_client) -> str:
        """
        Execute tool call
        
        Args:
            tool_use: Tool call details from LLM
            mcp_client: MCP client for tool execution
            
        Returns:
            Tool execution result
        """
        # Your implementation
        pass
```

4. Add to `providers/__init__.py`:
```python
from .your_provider import YourProvider
__all__ = [..., 'YourProvider']
```

5. Document environment variables in `.env.example`

## Environment Variables

Each provider should document its required environment variables:

### Bedrock
```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_API_KEY=your-key
```

### OpenRouter
```env
OPENROUTER_API_KEY=your-key
OPENROUTER_MODEL=anthropic/claude-3-sonnet
```

## Provider Configuration

Providers are configured in `providers/factory.py` which handles instantiation based on environment variables.
