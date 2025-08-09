import json
import requests
from typing import List, Dict, Any, Optional
from .base import LLMProvider

class OpenRouterProvider(LLMProvider):
    """OpenRouter LLM provider"""
    
    def __init__(self, api_key: str, model: str = "anthropic/claude-3-sonnet"):
        self.api_key = api_key
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"
    
    def ask(self, prompt: str, system_prompt: Optional[str] = None, 
            tools: Optional[List[Dict]] = None) -> Any:
        """Send request to OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = self._convert_tools(tools)
        
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        return response.json()
    
    def _convert_tools(self, bedrock_tools: List[Dict]) -> List[Dict]:
        """Convert Bedrock tool format to OpenAI format"""
        openai_tools = []
        for tool in bedrock_tools:
            if 'toolSpec' in tool:
                spec = tool['toolSpec']
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": spec['name'],
                        "description": spec['description'],
                        "parameters": spec['inputSchema']['json']
                    }
                })
        return openai_tools
    
    def handle_tool_call(self, tool_use: Dict, mcp_client) -> str:
        """Handle OpenRouter/OpenAI tool call format"""
        tool_name = tool_use['function']['name']
        tool_input = json.loads(tool_use['function']['arguments'])
        
        try:
            result = mcp_client.call_tool(tool_name, tool_input)
            if result and 'result' in result and 'content' in result['result']:
                return result['result']['content'][0]['text']
            return str(result)
        except Exception as e:
            return f"Tool {tool_name} failed: {str(e)}"
