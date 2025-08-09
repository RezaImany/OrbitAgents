# Example Agents

This directory contains reference agent implementations. These are provided as examples only - replace them with agents for your specific use case.

## What's Included

Example agents demonstrating the framework's capabilities. These can be used as templates for building your own agents.

## Creating Your Own Agents

Agents are simple to create:

```python
agent_registry.register_agent(
    name="your_agent",
    description="What your agent does",
    system_prompt="You are a specialized agent that...",
    mcp_client=mcp_client  # Optional: if agent needs tools
)
```

### Best Practices:

- Keep prompts focused and specific
- Define clear responsibilities
- Use structured output formats
- Handle edge cases gracefully
- Document expected inputs/outputs

## Example Use Cases

The framework can be adapted for any domain:
- Data analysis and reporting
- Content generation and review
- Research and information gathering
- Workflow automation
- Multi-step decision making
- Quality assurance and testing
