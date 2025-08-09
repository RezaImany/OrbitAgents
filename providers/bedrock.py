import json
import requests
from typing import List, Dict, Any, Optional
from .base import LLMProvider

class BedrockProvider(LLMProvider):
    """AWS Bedrock LLM provider"""
    
    def __init__(self, region: str, model_id: str, api_key: str):
        self.region = region
        self.model_id = model_id
        self.api_key = api_key
        self.url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/converse"
    
    def ask(self, prompt: str, system_prompt: Optional[str] = None, 
            tools: Optional[List[Dict]] = None) -> Any:
        """Send request to Bedrock"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 4096, "temperature": 0.7}
        }
        
        if system_prompt:
            payload["system"] = [{"text": system_prompt}]
        if tools:
            payload["toolConfig"] = {"tools": tools}
        
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        
        return response.json()
    
    def handle_tool_call(self, tool_use: Dict, mcp_client) -> str:
        """Handle Bedrock tool call format"""
        tool_name = tool_use['name']
        tool_input = tool_use.get('input', {})
        
        try:
            result = mcp_client.call_tool(tool_name, tool_input)
            if result and 'result' in result and 'content' in result['result']:
                return result['result']['content'][0]['text']
            return str(result)
        except Exception as e:
            return f"Tool {tool_name} failed: {str(e)}"
