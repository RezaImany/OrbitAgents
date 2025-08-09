import requests
import json


class MCPClient:
    def __init__(self, base_url="http://localhost:8000/mcp", api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def list_tools(self):
        """Get available tools from MCP server"""
        payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        print("LIST_TOOLS PAYLOAD:", payload)
        response = self.session.post(
            self.base_url,
            json=payload
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
        if response.text and response.status_code == 200:
            data = response.json()
            responseTools = data["result"]["tools"]
            tools = []
            for tool in responseTools:
                bedrock_tool = {
                    "toolSpec": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "inputSchema": {
                            "json": tool["inputSchema"]
                        }
                    }
                }
                tools.append(bedrock_tool)
            return tools
        return None
    
    def call_tool(self, tool_name, arguments=None):
        """Call a specific tool with arguments"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        print("CALL_TOOL PAYLOAD:", payload)
        response = self.session.post(self.base_url, json=payload)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
        if response.text and response.status_code == 200:
            return response.json()
        return None
