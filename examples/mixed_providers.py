"""
Mixed LLM Providers Example

Demonstrates using different LLM providers for different agents:
- Agent 1 uses Bedrock
- Agent 2 uses OpenRouter
- Orchestrator uses Bedrock
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient
from providers import BedrockProvider, OpenRouterProvider
from notifiers.factory import create_notifier

load_dotenv()

# Create multiple LLM providers
bedrock_provider = BedrockProvider(
    region=os.getenv('AWS_REGION', 'us-east-1'),
    model_id=os.getenv('BEDROCK_MODEL_ID'),
    api_key=os.getenv('BEDROCK_API_KEY')
)

openrouter_provider = OpenRouterProvider(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    model=os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-sonnet')
)

# Initialize notifier and MCP
notifier, channel = create_notifier()
mcp_client = MCPClient(
    base_url=os.getenv('MCP_SERVER_URL', 'http://localhost:8000/mcp'),
    api_key=os.getenv('MCP_API_KEY')
)

# Create registry with default provider
agent_registry = AgentToolRegistry(
    default_llm_provider=bedrock_provider,
    default_mcp_client=mcp_client
)

# Register agents with different providers
agent_registry.register_agent(
    name="bedrock_analyst",
    description="Analyzes data using AWS Bedrock",
    system_prompt="You are an analyst using AWS Bedrock. Provide insights.",
    llm_provider=bedrock_provider  # Explicitly use Bedrock
)

agent_registry.register_agent(
    name="openrouter_researcher",
    description="Researches topics using OpenRouter",
    system_prompt="You are a researcher using OpenRouter. Gather information.",
    llm_provider=openrouter_provider  # Explicitly use OpenRouter
)

agent_registry.register_agent(
    name="default_validator",
    description="Validates information using default provider",
    system_prompt="You are a validator. Check accuracy."
    # No llm_provider specified - uses default (Bedrock)
)

print("Registered agents:")
print(f"  - bedrock_analyst (Bedrock)")
print(f"  - openrouter_researcher (OpenRouter)")
print(f"  - default_validator (Bedrock - default)")

# Create orchestrator (uses Bedrock)
orchestrator = EnhancedOrchestrator(
    llm_provider=bedrock_provider,
    mcp_client=mcp_client,
    agent_registry=agent_registry,
    notifier=notifier
)

ORCHESTRATOR_PROMPT = """
You coordinate specialized agents with different LLM providers.

Available agents:
- bedrock_analyst: Uses AWS Bedrock for analysis
- openrouter_researcher: Uses OpenRouter for research
- default_validator: Uses default provider for validation

Delegate tasks to appropriate agents based on their capabilities.
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
    print(f"\nUsing Notifier: {os.getenv('NOTIFIER', 'console')}")
    print(f"Channel: {channel}\n")
    
    result = run("Research current trends and analyze the data")
    print(f"\nResult: {result}")
