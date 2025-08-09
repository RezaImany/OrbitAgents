"""
Generic agent examples demonstrating the framework.
Replace these with agents specific to your use case.
"""

# Example 1: Data Analyst Agent
agent_registry.register_agent(
    "data_analyst",
    "Analyzes data and identifies patterns",
    """
    You are a Data Analyst agent.
    Analyze data, identify trends, and provide insights.
    Keep responses concise and actionable.
    Use available tools to gather and process data.
    """,
    mcp_client=mcp_client
)

# Example 2: Researcher Agent
agent_registry.register_agent(
    "researcher",
    "Gathers and synthesizes information",
    """
    You are a Research agent.
    Gather information from available sources.
    Verify facts and provide accurate summaries.
    Focus on relevance and credibility.
    """,
    mcp_client=mcp_client
)

# Example 3: Validator Agent
agent_registry.register_agent(
    "validator",
    "Validates and verifies information",
    """
    You are a Validator agent.
    Check information for accuracy and consistency.
    Identify discrepancies or issues.
    Provide clear validation results.
    """,
    mcp_client=mcp_client
)
