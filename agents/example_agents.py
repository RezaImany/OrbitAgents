"""
Generic agent examples.
Copy and modify these for your specific use case.
"""

# Example: Data Analyst Agent
agent_registry.register_agent(
    "data_analyst",
    "Analyzes data and identifies patterns",
    """
    You are a Data Analyst agent.
    Analyze data, identify trends, and provide insights.
    Keep responses concise and actionable.
    """,
    mcp_client=mcp_client
)

# Example: Researcher Agent  
agent_registry.register_agent(
    "researcher",
    "Gathers and synthesizes information",
    """
    You are a Research agent.
    Gather information and provide accurate summaries.
    Focus on relevance and credibility.
    """,
    mcp_client=mcp_client
)
