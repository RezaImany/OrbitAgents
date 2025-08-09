# OrbitAgents Architecture

## Overview

This framework uses a **factory pattern** with **registry-based configuration** for maximum scalability. Adding new LLM providers or notifiers requires minimal code changes.

## Core Components

### 1. LLM Providers (`providers/`)

```
providers/
├── base.py           # Abstract interface
├── factory.py        # Provider registry & factory
├── bedrock.py        # AWS Bedrock implementation
├── openrouter.py     # OpenRouter implementation
└── README.md         # How to add providers
```

**Factory Pattern:**
- `factory.py` contains a `PROVIDERS` registry
- Each provider is registered with its class and configuration
- `create_llm_provider()` instantiates based on env vars
- Adding a new provider = add entry to registry

**Example:**
```python
# In factory.py
PROVIDERS = {
    'bedrock': {
        'class': BedrockProvider,
        'config': lambda: {...}
    },
    'your_provider': {  # Just add this!
        'class': YourProvider,
        'config': lambda: {...}
    }
}
```

### 2. Notifiers (`notifiers/`)

```
notifiers/
├── base.py           # Abstract interface
├── factory.py        # Notifier registry & factory
├── slack.py          # Slack implementation
├── telegram.py       # Telegram implementation
├── console.py        # Console implementation
└── README.md         # How to add notifiers
```

**Factory Pattern:**
- `factory.py` contains a `NOTIFIERS` registry
- Each notifier is registered with its class, config, and default channel
- `create_notifier()` instantiates based on env vars
- Adding a new notifier = add entry to registry

**Example:**
```python
# In factory.py
NOTIFIERS = {
    'slack': {
        'class': SlackNotifier,
        'config': lambda: {...},
        'channel': lambda: os.getenv('SLACK_CHANNEL')
    },
    'your_notifier': {  # Just add this!
        'class': YourNotifier,
        'config': lambda: {...},
        'channel': lambda: os.getenv('YOUR_CHANNEL')
    }
}
```

### 3. Agent System (`helpers/agent_tools.py`)

**AgentTool:**
- Wraps an LLM provider with specific system prompt
- Can access MCP tools
- Executes specialized tasks

**AgentToolRegistry:**
- Manages collection of agents
- Provides agents as tools to orchestrator
- Routes queries to appropriate agents

**EnhancedOrchestrator:**
- Coordinates multiple agents
- Uses LLM provider for decision making
- Streams results via notifier

### 4. MCP Client (`helpers/mcp_client.py`)

Connects to Model Context Protocol servers for external tools.

## Data Flow

```
1. User Query
   ↓
2. main.py calls factories
   ↓
3. create_llm_provider() → Provider instance
   create_notifier() → Notifier instance
   ↓
4. Orchestrator coordinates agents
   ↓
5. Agents execute (via LLM Provider + MCP tools)
   ↓
6. Results sent (via Notifier)
```

## Configuration Flow

```
Environment Variables (.env)
   ↓
Factory reads config
   ↓
Registry lookup
   ↓
Instance created
   ↓
Injected into orchestrator
```

## Scalability

### Adding 10+ LLM Providers

**Before (without factory):**
```python
# main.py would have 10+ if/elif blocks
if provider == 'bedrock':
    llm = BedrockProvider(...)
elif provider == 'openrouter':
    llm = OpenRouterProvider(...)
elif provider == 'openai':
    llm = OpenAIProvider(...)
# ... 7 more elif blocks
```

**After (with factory):**
```python
# main.py stays clean
llm_provider = create_llm_provider()

# All providers registered in factory.py
PROVIDERS = {
    'bedrock': {...},
    'openrouter': {...},
    'openai': {...},
    # ... add 100 more, main.py unchanged!
}
```

### Adding 10+ Notifiers

Same pattern - registry grows, main.py stays clean.

## Design Principles

1. **Registry Pattern**: All providers/notifiers in one place
2. **Factory Pattern**: Centralized instantiation logic
3. **Separation of Concerns**: main.py doesn't know about implementations
4. **Open/Closed Principle**: Open for extension, closed for modification
5. **Configuration over Code**: Behavior via environment variables

## Example: Adding a New Provider

### Step 1: Create Provider Class

```python
# providers/anthropic_direct.py
from .base import LLMProvider

class AnthropicDirectProvider(LLMProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    def ask(self, prompt, system_prompt=None, tools=None):
        # Implementation
        pass
    
    def handle_tool_call(self, tool_use, mcp_client):
        # Implementation
        pass
```

### Step 2: Register in Factory

```python
# providers/factory.py
from .anthropic_direct import AnthropicDirectProvider

PROVIDERS = {
    # ... existing providers
    'anthropic': {
        'class': AnthropicDirectProvider,
        'config': lambda: {
            'api_key': os.getenv('ANTHROPIC_API_KEY'),
            'model': os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet')
        }
    }
}
```

### Step 3: Update Environment Template

```bash
# .env.example
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-3-sonnet
```

### Step 4: Use It

```bash
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-...
```

**That's it!** No changes to `main.py` or any other code.

## Testing

Use `ConsoleNotifier` for testing without external services:

```bash
NOTIFIER=console
```

## Benefits

1. **Scalability**: Add unlimited providers/notifiers
2. **Maintainability**: Changes isolated to factory
3. **Testability**: Easy to mock factories
4. **Documentation**: Registry serves as documentation
5. **Validation**: Centralized config validation
6. **Discovery**: `list_providers()` and `list_notifiers()` functions

## Future Enhancements

- Auto-discovery of providers/notifiers
- Plugin system for external providers
- Configuration validation schemas
- Provider health checks
- Fallback providers
