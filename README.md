# 🪐 OrbitAgents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**OrbitAgents** is a flexible, open-source framework for orchestrating multiple AI agents. It empowers developers to build complex, multi-agent systems where each agent can utilize different LLM providers (Bedrock, OpenRouter, etc.) and specialized tools (MCP) to solve intricate tasks collaboratively.

---

## 🚀 Why OrbitAgents?

- **🧩 Agnostic & Pluggable**: Mix and match LLM providers (AWS Bedrock, OpenRouter, OpenAI) and notification channels (Slack, Telegram, Console).
- **🛠️ MCP Native**: First-class support for the Model Context Protocol (MCP) to give your agents superpowers.
- **🤖 Specialized Agents**: Create agents with distinct personalities, tools, and underlying models.
- **⚡ Viral-Ready**: Designed for speed, scalability, and ease of contribution.

## 🏗️ Architecture

```mermaid
graph LR
    User[User Query] --> Orch[Orchestrator]
    Orch --> A1[Agent 1<br/>(Bedrock)]
    Orch --> A2[Agent 2<br/>(OpenRouter)]
    Orch --> A3[Agent 3<br/>(Local)]
    A1 --> Res[Synthesized Result]
    A2 --> Res
    A3 --> Res
    Res --> Notifier[Notifier<br/>(Slack/Telegram)]
```

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run It
```bash
python main.py
```

## 🛠️ How to Build a Use Case

OrbitAgents is designed to be the backbone of your AI applications. Here is how you can build your own use case:

### 1. Create a Directory
Create a new directory for your project (e.g., `my_agent_app`).

### 2. Initialize Components
Import the necessary factories and helpers:

```python
from providers.factory import create_llm_provider
from notifiers.factory import create_notifier
from helpers.agent_tools import AgentToolRegistry, EnhancedOrchestrator
from helpers.mcp_client import MCPClient

# Initialize core components
llm_provider = create_llm_provider()
notifier, channel = create_notifier()
mcp_client = MCPClient(...)
```

### 3. Register Agents
Define your specialized agents. Each agent can have its own personality and tools.

```python
agent_registry = AgentToolRegistry(
    default_llm_provider=llm_provider,
    default_mcp_client=mcp_client
)

agent_registry.register_agent(
    name="analyst",
    description="Analyzes data and trends",
    system_prompt="You are an expert analyst..."
)
```

### 4. Create Orchestrator
The orchestrator manages the agents and handles the flow of information.

```python
orchestrator = EnhancedOrchestrator(
    llm_provider=llm_provider,
    mcp_client=mcp_client,
    agent_registry=agent_registry,
    notifier=notifier
)

# Run a query
response = orchestrator.ask("Analyze the Q3 sales data", channel=channel)
```

For a real-world example, check out the **Monitoring Assistant** use case in the `use-cases/` directory or the `examples/` folder.

## 📖 Documentation

- [**Quick Start Guide**](QUICKSTART.md): Get up and running in minutes.
- [**Architecture**](ARCHITECTURE.md): Deep dive into the factory pattern and core components.
- [**Contributing**](CONTRIBUTING.md): Join the community and help us build OrbitAgents.
- [**Security**](SECURITY.md): Best practices for keeping your agents secure.

## 🌟 Community & Support

OrbitAgents is an open-source project, and we welcome contributions from the community!

- **🐛 Issues**: Report bugs or request features on [GitHub Issues](https://github.com/rezallion/OrbitAgents/issues).
- **💬 Discussions**: Join the conversation (Coming Soon).
- **🗺️ Roadmap**: Check out what we're building next.

## 🤝 Contributing

We love contributors! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by the OrbitAgents Contributors
</p>
