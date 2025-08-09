import json
import requests
from typing import Optional

class BedrockToolClient:
    def __init__(self, region, profileid, api_key, mcp_client=None, enable_tools=False):
        self.region = region
        self.profileid = profileid
        self.api_key = api_key
        self.mcp_client = mcp_client
        self.tools = mcp_client.list_tools() if (enable_tools and mcp_client) else None

    def ask(self, prompt, system_prompt: Optional = None):
        url = f"https://bedrock-runtime.{self.region}.amazonaws.com/model/{self.profileid}/converse"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
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

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    return f"Error: {response.status_code} - {response.text}"
                
                result = response.json()
                assistant_message = result['output']['message']
                messages.append(assistant_message)
                
                tool_calls = [content for content in assistant_message['content'] if 'toolUse' in content]
                
                if not tool_calls:
                    text_content = [content for content in assistant_message['content'] if 'text' in content]
                    return text_content[0]['text'] if text_content else "No response"
                
                tool_results = []
                for tool_call in tool_calls:
                    tool_use = tool_call['toolUse']
                    tool_result = self._handle_tool_call(tool_use)
                    
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use['toolUseId'],
                            "content": [{"text": tool_result}]
                        }
                    })
                
                messages.append({"role": "user", "content": tool_results})
                
            except Exception as e:
                return f"Request failed: {str(e)}"
    
    def _handle_tool_call(self, tool_use):
        """Handle MCP tool calls"""
        if not self.mcp_client:
            return "No MCP client available for tool calls"
            
        tool_name = tool_use['name']
        tool_input = tool_use.get('input', {})
        
        try:
            result = self.mcp_client.call_tool(tool_name, tool_input)
            if result and 'result' in result and 'content' in result['result']:
                return result['result']['content'][0]['text']
            return str(result)
        except Exception as e:
            return f"Tool {tool_name} failed: {str(e)}"
