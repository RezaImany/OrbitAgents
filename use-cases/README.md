# Use Cases

This directory contains real-world implementations using the AI Agent Orchestration Framework.

## Available Use Cases

### Monitoring Assistant (`monitoring-assistant/`)

Monitoring assistant for system monitoring and triage.

**What it does:**
- Monitors KPIs
- Detects service errors
- Correlates deployments with issues
- Analyzes dashboard metrics
- Sends alerts to Slack

**Run it:**
```bash
cd monitoring-assistant
python monitoring_orchestrator.py
```

See [monitoring-assistant/README.md](monitoring-assistant/README.md) for details.

## Creating Your Own Use Case

### 1. Create Directory

```bash
mkdir use-cases/your-use-case
cd use-cases/your-use-case
```

### 2. Create Main Script

```python
import sys
sys.path.insert(0, '../..')

from providers.factory import create_llm_provider
from notifiers.factory import create_notifier
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient

# Initialize
llm_provider = create_llm_provider()
notifier, channel = create_notifier()
mcp_client = MCPClient(...)

# Create agents
agent_registry = AgentToolRegistry(
    default_llm_provider=llm_provider,
    default_mcp_client=mcp_client
)

agent_registry.register_agent("agent1", "...", "...")
agent_registry.register_agent("agent2", "...", "...")

# Create orchestrator
orchestrator = EnhancedOrchestrator(
    llm_provider, mcp_client, agent_registry, notifier
)

# Run
response = orchestrator.ask("Your query", channel=channel)
```

### 3. Add Configuration

```bash
cp ../../.env.example .env
# Edit .env
```

### 4. Document

Create `README.md` explaining:
- What the use case does
- How to set it up
- How to run it
- How to customize it

## Use Case Ideas

- **Customer Support** - Route queries to specialized support agents
- **Data Pipeline** - Monitor ETL jobs and data quality
- **Security** - Incident response and threat analysis
- **DevOps** - Infrastructure monitoring and automation
- **Business Intelligence** - Automated reporting and analysis
- **Content Moderation** - Multi-stage content review
- **Research** - Automated literature review and synthesis
- **Testing** - Automated test generation and execution

## Benefits

- **Reusable Framework** - Don't rebuild orchestration logic
- **Pluggable Components** - Swap LLMs and notifiers easily
- **MCP Integration** - Connect to any tools
- **Maintainable** - Clean separation of concerns
- **Scalable** - Add agents without changing core code

## Contributing

Have a use case to share? Submit a PR with:
- Implementation in `use-cases/your-use-case/`
- README documenting setup and usage
- `.env.example` with required configuration
- Example queries and expected outputs
