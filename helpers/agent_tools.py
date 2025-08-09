import logging
import json
import requests

logger = logging.getLogger(__name__)

class AgentTool:
    """Agent with its own LLM provider and optional MCP tools"""
    
    def __init__(self, name, description, llm_provider, mcp_client=None, system_prompt=None):
        self.name = name
        self.description = description
        self.llm_provider = llm_provider
        self.mcp_client = mcp_client
        self.system_prompt = system_prompt or f"You are {name}. {description}"
    
    def execute(self, user_input):
        """Execute agent with user input"""
        from .bedrock_tool_client import BedrockToolClient
        
        # Use BedrockToolClient for proper tool handling
        if hasattr(self.llm_provider, 'region'):  # It's a Bedrock provider
            client = BedrockToolClient(
                self.llm_provider.region,
                self.llm_provider.model_id,
                self.llm_provider.api_key,
                self.mcp_client,
                enable_tools=True
            )
            return client.ask(user_input, system_prompt=self.system_prompt)
        else:
            # For other providers, simple call
            tools = self.mcp_client.list_tools() if self.mcp_client else None
            return self.llm_provider.ask(user_input, system_prompt=self.system_prompt, tools=tools)
    
    def to_tool_spec(self):
        """Convert agent to tool specification"""
        return {
            "toolSpec": {
                "name": self.name,
                "description": self.description,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The query or task for the agent"
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        }

class AgentToolRegistry:
    """Registry for managing agents with different LLM providers"""
    
    def __init__(self, default_llm_provider=None, default_mcp_client=None):
        self.default_llm_provider = default_llm_provider
        self.default_mcp_client = default_mcp_client
        self.agents = {}
    
    def register_agent(self, name, description, system_prompt=None, 
                      llm_provider=None, mcp_client=None):
        """Register a new agent with optional custom LLM provider"""
        agent = AgentTool(
            name, 
            description, 
            llm_provider or self.default_llm_provider,
            mcp_client or self.default_mcp_client,
            system_prompt
        )
        self.agents[name] = agent
        return agent
    
    def get_agent_tools(self):
        """Get all agents as tool specs"""
        return [agent.to_tool_spec() for agent in self.agents.values()]
    
    def call_agent(self, agent_name, query):
        """Call a specific agent"""
        if agent_name in self.agents:
            return self.agents[agent_name].execute(query)
        return f"Agent '{agent_name}' not found"

class EnhancedOrchestrator:
    """Orchestrator that coordinates agents with full tool calling support"""
    
    def __init__(self, llm_provider, mcp_client, agent_registry, notifier=None):
        self.llm_provider = llm_provider
        self.mcp_client = mcp_client
        self.agent_registry = agent_registry
        self.notifier = notifier
        self.tools = agent_registry.get_agent_tools() if agent_registry else []
    
    def _is_important_result(self, result):
        """Check if agent result is important"""
        if not result:
            return False
        result_lower = result.lower()
        if "alert" in result_lower:
            return True
        if "normal" in result_lower and "none" in result_lower:
            return False
        return True
    
    def ask(self, prompt, system_prompt=None, verbose=False, agent_verbose=False, channel=None):
        """Run orchestrator with full tool calling loop"""
        if verbose and self.notifier and channel:
            self.notifier.send_message(channel, f"🔍 **Starting**: {prompt}", create_thread=True)
        
        # For Bedrock, use full tool calling loop
        if hasattr(self.llm_provider, 'region'):
            url = f"https://bedrock-runtime.{self.llm_provider.region}.amazonaws.com/model/{self.llm_provider.model_id}/converse"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.llm_provider.api_key}"
            }
            
            messages = [{"role": "user", "content": [{"text": prompt}]}]
            
            while True:
                payload = {
                    "messages": messages,
                    "inferenceConfig": {"maxTokens": 4096, "temperature": 0.7}
                }
                
                if system_prompt:
                    payload["system"] = [{"text": system_prompt}]
                if self.tools:
                    payload["toolConfig"] = {"tools": self.tools}
                
                resp = requests.post(url, headers=headers, json=payload)
                response_data = resp.json()
                
                assistant_message = response_data.get('output', {}).get('message', response_data)
                
                if isinstance(assistant_message, str):
                    if verbose and self.notifier and channel:
                        self.notifier.send_message(channel, f"✅ **Final Result**:\n{assistant_message}", broadcast_final=True)
                    return assistant_message
                
                messages.append(assistant_message)
                
                tool_calls = [c for c in assistant_message.get('content', []) if 'toolUse' in c]
                
                if not tool_calls:
                    text_content = [c for c in assistant_message.get('content', []) if 'text' in c]
                    final_result = text_content[0]['text'] if text_content else "No response"
                    if verbose and self.notifier and channel:
                        self.notifier.send_message(channel, f"✅ **Final Result**:\n{final_result}", broadcast_final=True)
                    return final_result
                
                tool_results = []
                for tool_call in tool_calls:
                    tool_use = tool_call['toolUse']
                    tool_name = tool_use['name']
                    tool_input = tool_use['input']
                    
                    is_agent_call = tool_name in self.agent_registry.agents
                    
                    if verbose and self.notifier and is_agent_call and channel:
                        self.notifier.send_message(channel, f"🔧 **Calling**: {tool_name}")
                    
                    if is_agent_call:
                        result = self.agent_registry.call_agent(tool_name, tool_input.get('query', ''))
                        tool_content = result
                        
                        if verbose and self.notifier and channel:
                            if agent_verbose or self._is_important_result(tool_content):
                                self.notifier.send_message(channel, f"📊 **{tool_name} Result**: {tool_content}")
                    else:
                        # Direct MCP tool call
                        result = self.mcp_client.call_tool(tool_name, tool_input)
                        tool_content = result['result']['content'][0]['text'] if result else "Tool call failed"
                        
                        if agent_verbose and verbose and self.notifier and channel:
                            self.notifier.send_message(channel, f"🔧 **MCP Tool**: {tool_name}")
                            self.notifier.send_message(channel, f"📊 **Result**: {tool_content}")
                    
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use['toolUseId'],
                            "content": [{"text": tool_content}]
                        }
                    })
                
                messages.append({"role": "user", "content": tool_results})
        else:
            # For other providers, simple call
            response = self.llm_provider.ask(prompt, system_prompt=system_prompt, tools=self.tools)
            if verbose and self.notifier and channel:
                self.notifier.send_message(channel, f"✅ **Final Result**:\n{response}", broadcast_final=True)
            return response
