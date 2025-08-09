# OrbitAgents Changelog

## v2.0.0 - Pluggable Architecture

### Major Changes
- ✅ **Pluggable LLM Providers**: Support for multiple LLM backends
  - AWS Bedrock
  - OpenRouter
  - Easy to add: OpenAI, Anthropic Direct, Azure, local models
  
- ✅ **Pluggable Notifiers**: Support for multiple notification channels
  - Slack
  - Telegram
  - Console (for testing)
  - Easy to add: Discord, Teams, Email, Webhooks

### Architecture
- ✅ Created `providers/` directory with base interface
- ✅ Created `notifiers/` directory with base interface
- ✅ Refactored `agent_tools.py` to use dependency injection
- ✅ Environment-based configuration for runtime selection

### Documentation
- ✅ Added ARCHITECTURE.md explaining pluggable design
- ✅ Updated README with provider/notifier examples
- ✅ Added extension guides for custom providers

## v1.0.0 - Open Source Release

### Security
- ✅ Removed all hardcoded credentials
- ✅ Added environment variable configuration
- ✅ Created .env.example template
- ✅ Added .gitignore for sensitive files
- ✅ Added SECURITY.md with best practices

### Generalization
- ✅ Removed vendor-specific references
- ✅ Removed company-specific code
- ✅ Made all examples generic
- ✅ Renamed lambda_function.py → main.py
- ✅ Created generic agent templates

### Documentation
- ✅ README focused on agent orchestration concept
- ✅ Added CONTRIBUTING.md
- ✅ Added LICENSE (MIT)
- ✅ Added example implementations

### Structure
- ✅ Organized examples/ directory
- ✅ Clean project structure
- ✅ Version-pinned dependencies
- ✅ Modular, extensible design
