import os
import logging
from dotenv import load_dotenv
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient
from providers.factory import create_llm_provider
from notifiers.factory import create_notifier

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize components using factories
llm_provider = create_llm_provider()
notifier, default_channel = create_notifier()

logger.info(f"Using LLM provider: {os.getenv('LLM_PROVIDER', 'bedrock')}")
logger.info(f"Using notifier: {os.getenv('NOTIFIER', 'console')}")

# Initialize MCP and Agent Registry
mcp_client = MCPClient(
    base_url=os.getenv('MCP_SERVER_URL', 'http://localhost:8000/mcp'),
    api_key=os.getenv('MCP_API_KEY')
)

# Registry with default provider (agents can override)
agent_registry = AgentToolRegistry(
    default_llm_provider=llm_provider,
    default_mcp_client=mcp_client
)

def load_agents(agent_dir='agents'):
    """Load agent definitions from directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agents_path = os.path.join(script_dir, agent_dir)
    
    if not os.path.exists(agents_path):
        logger.warning(f"Agents directory not found: {agents_path}")
        return
    
    for filename in os.listdir(agents_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            filepath = os.path.join(agents_path, filename)
            try:
                exec(open(filepath).read())
                logger.info(f"Loaded {filename}")
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")

load_agents()
logger.info(f"Registered {len(agent_registry.agents)} agents")

# Create orchestrator
orchestrator = EnhancedOrchestrator(
    llm_provider=llm_provider,
    mcp_client=mcp_client,
    agent_registry=agent_registry,
    notifier=notifier
)

def run(query, system_prompt=None, verbose=True, agent_verbose=False, channel=None):
    """
    Run orchestrator with query
    
    Args:
        query: Task or question
        system_prompt: Custom orchestrator prompt
        verbose: Show orchestrator activity
        agent_verbose: Show detailed agent calls
        channel: Notification channel (defaults to env var)
    """
    channel = channel or default_channel
    return orchestrator.ask(
        query,
        system_prompt=system_prompt,
        verbose=verbose,
        agent_verbose=agent_verbose,
        channel=channel
    )

if __name__ == "__main__":
    default_prompt = """
You coordinate specialized agents to solve complex tasks.
Analyze requests, delegate to appropriate agents, and synthesize results.
Keep responses clear and actionable.
"""
    
    response = run(
        "Analyze the current situation",
        system_prompt=default_prompt,
        verbose=True,
        agent_verbose=False
    )
    
    print(response)
