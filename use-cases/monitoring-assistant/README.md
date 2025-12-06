# Monitoring Assistant Use Case

This demonstrates using the AI Agent Orchestration Framework for monitoring assistance in system monitoring and triage.

## Overview

A monitoring assistant that:
- Monitors KPIs across data sources
- Detects service errors and faults
- Correlates deployments with issues
- Analyzes dashboard metrics
- Sends alerts to Slack

## Architecture

```
Monitoring Query → Orchestrator → kpi_analyst (checks metrics)
                        → error_analyst (checks errors)
                        → deployment_analyst (checks deployments)
                        → dashboard_analyst (checks dashboards)
                        ↓
                   Synthesized Alert → Slack
```

## Setup

### 1. Install Framework

```bash
cd ../..
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. MCP Server

This use case requires an MCP server providing monitoring tools:
- `kpi_observability_tool1` - Observability tool1 metrics
- `kpi_observability_tool2` - Observability tool2 metrics
- `error_detection` - Error detection
- `deployment_history_observability_tool1` - Deployment history
- `dashboard_search_observability_tool2` - Dashboard search
- `widget_analysis_observability_tool2` - Widget analysis
- `query_execution_observability_tool2` - Query execution

### 4. Run

```bash
python monitoring_orchestrator.py
```

## Agents

### kpi_analyst
Monitors KPI trends using observability tool1 and tool2.
- Detects drops/spikes >10%
- Compares data sources
- Severity tiers: HIGH ≥30%, MED 15–29%, LOW 10–14%

### error_analyst
Detects service errors and fault patterns.
- Identifies services with >100 errors/min
- Detects error spikes

### deployment_analyst
Correlates deployments with system issues.
- Checks recent deployments
- Identifies faulty deployments
- Suggests rollbacks

### dashboard_analyst
Analyzes dashboard metrics for anomalies.
- Searches dashboards by name
- Checks widgets for drops >10%

## Example Queries

```python
# Check platform health
check_platform("Check platform KPI and faulty services")

# Analyze specific dashboard
check_platform("Analyze 'Customer Journey Flow' dashboard")

# Regional check
check_platform("Why is search lower for EU today?")
```

## Customization

### Add New Agent

```python
agent_registry.register_agent(
    "your_agent",
    "Description",
    "System prompt...",
    mcp_client=mcp_client
)
```

### Change LLM Provider

```env
# Use OpenRouter instead of Bedrock
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your-key
```

### Change Notifier

```env
# Use Telegram instead of Slack
NOTIFIER=telegram
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_CHAT_ID=your-chat-id
```

## Integration

### Lambda Function

Deploy as AWS Lambda:

```python
def lambda_handler(event, context):
    query = event.get('query', 'Check platform health')
    response = check_platform(query, verbose=True)
    return {'statusCode': 200, 'body': response}
```

### Scheduled Checks

Run periodic checks:

```bash
# Cron: every 5 minutes
*/5 * * * * cd /path/to/use-case && python monitoring_orchestrator.py
```

### API Endpoint

Expose as API:

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check():
    query = request.json.get('query')
    response = check_platform(query)
    return {'response': response}
```

## Benefits of Using Framework

1. **Pluggable LLMs** - Switch providers without code changes
2. **Pluggable Notifiers** - Change notification channels easily
3. **Reusable Agents** - Agents work across use cases
4. **MCP Integration** - Connect to any monitoring tools
5. **Maintainable** - Clean separation of concerns

## Adapting for Your Use Case

This monitoring example shows the pattern. Adapt for:
- Customer support automation
- Data pipeline monitoring
- Security incident response
- DevOps automation
- Business intelligence

Just change the agents and MCP tools!
