# OrbitAgents Security Policy

## Supported Versions

Currently supporting the latest version with security updates.

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email the maintainers directly with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### Credentials Management
- Never commit `.env` files or credentials
- Use environment variables for all sensitive data
- Rotate API keys and tokens regularly
- Use least-privilege access for all services

### API Keys
- **AWS Bedrock**: Use IAM roles when possible, API keys as fallback
- **Slack**: Limit token scopes to required permissions only
- **MCP Server**: Use authentication and HTTPS in production

### Network Security
- Run MCP servers on localhost or private networks
- Use HTTPS for all external communications
- Implement rate limiting on API endpoints

### Code Security
- Keep dependencies updated
- Review agent prompts for potential injection risks
- Validate all user inputs
- Sanitize data before sending to Slack

### Slack Integration
- Use bot tokens (xoxb-) not user tokens
- Limit channel access appropriately
- Don't post sensitive data to public channels
- Implement message sanitization

## Known Security Considerations

1. **Prompt Injection**: Agents use LLMs which may be susceptible to prompt injection. Validate and sanitize inputs.

2. **Tool Access**: Agents with MCP access can execute tools. Ensure MCP tools are properly secured.

3. **Slack Messages**: Data sent to Slack is visible to channel members. Don't expose sensitive information.

4. **API Rate Limits**: Implement rate limiting to prevent abuse.

## Updates

Security updates will be released as needed. Watch the repository for notifications.
