"""
Simple Agent Orchestration Example

Demonstrates:
1. Creating specialized agents
2. Registering with orchestrator
3. Coordinating agents to solve tasks
4. Streaming results to notification channel
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient
from providers.factory import create_llm_provider
from notifiers.factory import create_notifier

load_dotenv()

# Initialize using factories
llm_provider = create_llm_provider()
notifier, channel = create_notifier()

print(f"Using LLM Provider: {os.getenv('LLM_PROVIDER', 'bedrock')}")
print(f"Using Notifier: {os.getenv('NOTIFIER', 'console')}")
print(f"Channel: {channel}\n")

# Initialize MCP and Agent Registry
mcp_client = MCPClient(
    base_url=os.getenv('MCP_SERVER_URL', 'http://localhost:8000/mcp'),
    api_key=os.getenv('MCP_API_KEY')
)
agent_registry = AgentToolRegistry(llm_provider, mcp_client)

# Register agents
agent_registry.register_agent(
    "analyst",
    "Analyzes data and identifies patterns",
    "You are an analyst. Analyze information and provide clear insights.",
    mcp_client=mcp_client
)

agent_registry.register_agent(
    "researcher",
    "Gathers and synthesizes information",
    "You are a researcher. Gather information and provide accurate summaries.",
    mcp_client=mcp_client
)

agent_registry.register_agent(
    "validator",
    "Validates and verifies information",
    "You are a validator. Check information for accuracy and consistency.",
    mcp_client=mcp_client
)

# Create orchestrator
orchestrator = EnhancedOrchestrator(
    llm_provider=llm_provider,
    mcp_client=mcp_client,
    agent_registry=agent_registry,
    notifier=notifier
)

# Orchestrator prompt
ORCHESTRATOR_PROMPT = """
You coordinate specialized agents to solve tasks.

Available agents:
- analyst: Analyzes data and patterns
- researcher: Gathers information
- validator: Validates accuracy

Delegate tasks appropriately and synthesize results.
Keep responses clear and concise.
"""

def run(query, verbose=True):
    """Run orchestrator with query"""
    return orchestrator.ask(
        query,
        system_prompt=ORCHESTRATOR_PROMPT,
        verbose=verbose,
        channel=channel
    )

if __name__ == "__main__":
    result = run("Analyze the current situation and provide recommendations")
    print(f"\nResult: {result}")
