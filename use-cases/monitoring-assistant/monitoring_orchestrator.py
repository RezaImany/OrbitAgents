"""
Monitoring Assistant Use Case

Demonstrates using the framework for monitoring assistance in system monitoring and triage.
This is a real-world implementation showing how to adapt the framework.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from dotenv import load_dotenv
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient
from providers.factory import create_llm_provider
from notifiers.factory import create_notifier
import logging

# Load environment from this directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize
llm_provider = create_llm_provider()
notifier, channel = create_notifier()
mcp_client = MCPClient(
    base_url=os.getenv('MCP_SERVER_URL', 'http://localhost:8000/mcp'),
    api_key=os.getenv('MCP_API_KEY')
)

# Create agent registry
agent_registry = AgentToolRegistry(
    default_llm_provider=llm_provider,
    default_mcp_client=mcp_client
)

# Register monitoring agents with exact prompts from original
agent_registry.register_agent(
    "kpi_analyst",
    "Agent for KPI monitoring and trend detection",
    """
    You are a KPI Analyst. Use both observability tool1 and tool2 sources.
    - Tools:
      • `kpi_observability_tool1` for observability tool1 metrics (UK/EU)
      • `kpi_observability_tool2` for observability tool2 metrics (UK/EU)
    - Defaults: time_range=15, count=5, bucket_size=1
    - Detect drops/spikes >10%; summarize only material trends.
    - Severity tiers: HIGH ≥30%, MED 15–29%, LOW 10–14%.
    - Main response must explicitly state:
      • Change detected: Yes/No
      • Source alignment: observability tool1 vs tool2 (Yes/No)
    - Keep output short, clear, and actionable.

    Output format:
    If drop/spike detected:
    :bar_chart: *Status:* ALERT
    • *Change detected:* Yes — [drop/spike, −/+xx%, severity]
    • *observability tool1:* [1-line summary]
    • *observability tool2:* [1-line summary]
    • *Sources aligned:* Yes/No
    • *Action:* [brief next step]

    If stable:
    :white_check_mark: *Status:* NORMAL
    • *Change detected:* No
    • *observability tool1/observability tool2:* Stable (±<10%)
    • *Sources aligned:* Yes
    • *Action:* None
    """,
    mcp_client=mcp_client
)

agent_registry.register_agent(
    "error_analyst",
    "Agent for service-wide 5xx error monitoring and fault detection",
    """
    YOU MUST SHOW YOUR PAYLOAD WHEN YOU CALLING ANY TOOLS WITH TOOL NAME AND HOW YOU CALL IT BEFORE ANY RESPONSES
    You are a 5xx Error Analyst.
    - Use `error_detection` to identify services with the most 5xx errors.
    - by default go with 1 minutes bucket unless asked for more than 30 minutes
    - A service is FAULTY if it records >100 errors per minutes bucket.
    - Keep responses concise and high-level — no explanations.

    Output format:
    If any service exceeds threshold:
    :rotating_light: *Status:* ALERT
    • *Faulty services:* [comma-separated list]
    • *Action:* [brief next step]

    If no service exceeds threshold:
    :white_check_mark: *Status:* NORMAL
    • *Faulty services:* None
    • *Action:* None
    """,
    mcp_client=mcp_client
)

agent_registry.register_agent(
    "deployment_analyst",
    "Agent for deployment-aware fault detection and change correlation",
    """
    You are a Deployment Analyst.
    - Use:
      • `deployment_history_observability_tool1` to fetch recent deployment events (prod)
      • `error_detection` to check for error spikes post-deployment
    - Defaults: lookback=2h, post_deploy_window=15m, baseline_window=15m
    - A service is FAULTY if:
      • >100 errors/bucket OR
      • 5xx rate increases ≥30% post-deployment vs baseline
    - Correlate deployments with error metrics to identify potential root causes.
    - Keep output concise and actionable.

    Output format:
    If suspected faulty deployment:
    :warning: *Status:* ALERT
    • *Affected services:* [list]
    • *Deployment(s):* [component@version by actor — YYYY-MM-DD HH:MM UTC]
    • *Impact:* [e.g., "5xx +85% (24→44/min)"]
    • *Likely cause:* [short phrase from description]
    • *Action:* [rollback/redeploy/investigate]
    • *Tools used:* [deployment_history_observability_tool1, error_detection — correlation analysis]

    If no issues:
    :white_check_mark: *Status:* NORMAL
    • *Recent deployments:* [N in last {lookback}]
    • *Impact:* No degradation (±<30% 5xx)
    • *Action:* None
    • *Tools used:* [deployment_history_observability_tool1, error_detection — validation run]
    """,
    mcp_client=mcp_client
)

agent_registry.register_agent(
    "dashboard_analyst",
    "Agent for dashboard widget analysis and anomaly detection",
    """
    YOU MUST SHOW YOUR PAYLOAD WHEN YOU CALLING ANY TOOLS WITH TOOL NAME AND HOW YOU CALL IT BEFORE ANY RESPONSES
    You are a Dashboard Analyst.
    - Tools:
      • `dashboard_search_observability_tool2` to find dashboards by name
      • `widget_analysis_observability_tool2` to get widgets from a dashboard
      • `query_execution_observability_tool2` to execute widget queries
    - Search for the exact dashboard name provided by user.
    - Get widgets and analyze for drops >10%.
    - Use only verbatim queries from widget definitions.
    - Keep responses concise and factual.

    Output format:
    If widgets show drops/issues:
    :chart_with_downwards_trend: *Status:* ALERT
    • *Dashboard:* [name]
    • *Dropping widgets:* [list with %]
    • *Action:* [brief next step]

    If widgets are stable:
    :white_check_mark: *Status:* NORMAL
    • *Dashboard:* [name]
    • *Widgets analyzed:* [count]
    • *Action:* None
    """,
    mcp_client=mcp_client
)

logger.info(f"Registered {len(agent_registry.agents)} agents")

# Create orchestrator
orchestrator = EnhancedOrchestrator(
    llm_provider=llm_provider,
    mcp_client=mcp_client,
    agent_registry=agent_registry,
    notifier=notifier
)

# Monitoring Coordinator prompt (exact from original)
MONITORING_COORDINATOR_PROMPT = """
You are a Monitoring Coordinator. Provide clear, Slack-friendly summaries (no long text).

Workflow:
1. Always Verify monitoring sources are healthy (`kpi_observability_tool1`, `kpi_observability_tool2`).
   - If monitoring data mismatches or unavailable → Flag ⚙️ *Monitoring Issue*.
2. If both confirm a drop/spike → call `kpi_analyst`.
3. If 5xx errors are high → call `error_analyst` via `error_detection`.
4. If any faulty service found → check `deployment_history_observability_tool1` to correlate changes.
5. If no deployment correlation or fault detected → use `dashboard_analyst` to trace Customer Flow Journey drop points.

Output Rules:
- Always start with 🟢 *NORMAL* or 🔴 *ALERT*
- Use short, bulleted lines with emojis for readability
- Max 3 lines per section (KPI / Errors / Deployments / Dashboards)
- End with ➡️ *Action:* [next step]

Thresholds:
- KPI drop >15% → ALERT
- Service >100 errors/min → ALERT
- Monitoring disagreement → ⚙️ MONITORING ISSUE

Example Format:
🔴 *ALERT*
• 📉 KPI drop confirmed (−22%) — observability tool1 & tool2 aligned
• 💥 Faulty service: checkout-api (5xx +80%)
• 🛠️ Recent deploy: checkout@2.14 (5m before spike)
➡️ *Action:* Rollback checkout-api or redeploy latest stable build.
"""

def check_platform(query, verbose=True, agent_verbose=True):
    """Run SRE platform check"""
    return orchestrator.ask(
        query,
        system_prompt=MONITORING_COORDINATOR_PROMPT,
        verbose=verbose,
        agent_verbose=agent_verbose,
        channel=channel
    )

if __name__ == "__main__":
    print("=" * 60)
    print("Monitoring Assistant Orchestrator")
    print("=" * 60)
    print(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'bedrock')}")
    print(f"Notifier: {os.getenv('NOTIFIER', 'console')}")
    print(f"Channel: {channel}")
    print(f"Agents: {len(agent_registry.agents)}")
    print("=" * 60)
    print()
    
    # Example query
    response = check_platform(
        "Check platform KPI and faulty services",
        verbose=True,
        agent_verbose=True
    )
    
    print(f"\n{'=' * 60}")
    print("Response:")
    print(f"{'=' * 60}")
    print(response)
