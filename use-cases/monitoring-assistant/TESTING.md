# Testing Monitoring Assistant Use Case

This use case is fully configured and ready to test with your actual credentials.

## ✅ What's Configured

- **LLM Provider**: AWS Bedrock (eu-west-1)
- **Model**: Claude 3.7 Sonnet
- **Notifier**: Slack (#test)
- **MCP Server**: localhost:8000
- **All 4 Monitoring Agents**: kpi_analyst, error_analyst, deployment_analyst, dashboard_analyst

## 🚀 Quick Test

### Option 1: Direct Run

```bash
cd use-cases/monitoring-assistant
python3 monitoring_orchestrator.py
```

### Option 2: Test Script

```bash
cd use-cases/monitoring-assistant
./test_monitoring.sh
```

## 📋 What It Does

When you run it, the orchestrator will:

1. Initialize with your Bedrock credentials
2. Connect to Slack (#test)
3. Register 4 Monitoring agents
4. Execute query: "Check platform KPI and faulty services"
5. Coordinate agents to:
   - Check KPIs (observability tool1 + tool2)
   - Check for service errors
   - Check recent deployments
   - Analyze dashboards if needed
6. Send results to Slack
7. Print response to console

## 🔍 Expected Flow

```
1. Orchestrator receives query
   ↓
2. Calls kpi_analyst
   → Uses MCP tools: kpi_observability_tool1, kpi_observability_tool2
   ↓
3. Calls error_analyst
   → Uses MCP tool: error_detection
   ↓
4. Calls deployment_analyst (if errors found)
   → Uses MCP tools: deployment_history_observability_tool1, error_detection
   ↓
5. Synthesizes results
   ↓
6. Sends to Slack: 🟢 NORMAL or 🔴 ALERT
```

## 📊 Example Output

**Console:**
```
============================================================
Monitoring Assistant Orchestrator
============================================================
LLM Provider: bedrock
Notifier: slack
Channel: #test
Agents: 4
============================================================

INFO:__main__:Registered 4 agents
INFO:__main__:Using LLM provider: bedrock
INFO:__main__:Using notifier: slack

============================================================
Response:
============================================================
🟢 *NORMAL*
• 📊 KPIs stable (±5%)
• ✅ No faulty services detected
• 🛠️ Recent deployments: 3 (no impact)
➡️ *Action:* Continue monitoring
```

**Slack (#test):**
```
🔍 Starting: Check platform KPI and faulty services

🔧 Calling: kpi_analyst
📊 kpi_analyst Result: [analysis]

🔧 Calling: error_analyst
📊 error_analyst Result: [analysis]

✅ Final Result: [synthesized response]
```

## 🧪 Test Queries

Try these queries:

```python
# Basic health check
check_platform("Check platform KPI and faulty services")

# Dashboard analysis
check_platform("Analyze 'Customer Journey Flow' dashboard")

# Regional check
check_platform("Why is search lower for EU today?")

# Deployment check
check_platform("Check recent deployments and their impact")
```

## 🔧 Customization

### Change Notifier to Console (for testing without Slack)

Edit `.env`:
```env
NOTIFIER=console
```

### Change LLM Provider

Edit `.env`:
```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your-key
```

### Modify Agents

Edit `monitoring_orchestrator.py` and change agent prompts or add new agents.

## 🐛 Troubleshooting

### MCP Server Not Running

```
Error: Connection refused to localhost:8000
```

**Solution**: Start your MCP server or change MCP_SERVER_URL in `.env`

### Slack Token Invalid

```
Error: invalid_auth
```

**Solution**: Check SLACK_TOKEN in `.env`

### Bedrock API Key Expired

```
Error: 403 Forbidden
```

**Solution**: Generate new Bedrock API key and update BEDROCK_API_KEY in `.env`

## 📝 Notes

- This uses the **exact same agents and prompts** from your original implementation
- All credentials are in `.env` (not committed to git)
- The framework handles all the orchestration, you just define agents
- You can swap LLM providers or notifiers without changing agent code

## ✨ Benefits of Using Framework

Compare to original hardcoded implementations:

**Before (Original):**
- Hardcoded credentials
- Tightly coupled to specific providers
- Tightly coupled to specific notifiers
- Hard to test locally
- Hard to add new agents

**After (Framework):**
- ✅ Environment-based config
- ✅ Pluggable LLM providers
- ✅ Pluggable notifiers
- ✅ Easy to test (console notifier)
- ✅ Easy to add agents (just register)

## 🎯 Next Steps

1. Run the test
2. Check Slack for results
3. Try different queries
4. Modify agents for your needs
5. Add new agents
6. Deploy to Lambda (see README.md)
