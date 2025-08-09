# OrbitAgents Quick Start Guide

Get up and running in 5 minutes.

## 1. Install

```bash
pip install -r requirements.txt
```

## 2. Configure

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Choose provider
LLM_PROVIDER=bedrock
BEDROCK_API_KEY=your-key

# Choose notifier
NOTIFIER=console
```

## 3. Run

### Standalone

```bash
python main.py
```

### In Your Code

```python
from providers.factory import create_llm_provider
from notifiers.factory import create_notifier
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient

# Initialize
llm_provider = create_llm_provider()
notifier, channel = create_notifier()
mcp_client = MCPClient('http://localhost:8000/mcp', 'key')

# Create agents
agent_registry = AgentToolRegistry(default_llm_provider=llm_provider)
agent_registry.register_agent("analyst", "Analyzes data", "You are an analyst.")

# Create orchestrator
orchestrator = EnhancedOrchestrator(
    llm_provider, mcp_client, agent_registry, notifier
)

# Run
response = orchestrator.ask("Analyze this", verbose=True, channel=channel)
```

## 4. Examples

```bash
# Simple example
python examples/simple_orchestrator.py

# Mixed providers
python examples/mixed_providers.py
```

## Next Steps

- Read [README.md](README.md) for full documentation
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Check [providers/README.md](providers/README.md) to add LLM providers
- Check [notifiers/README.md](notifiers/README.md) to add notifiers
