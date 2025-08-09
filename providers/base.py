from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def ask(self, prompt: str, system_prompt: Optional[str] = None, 
            tools: Optional[List[Dict]] = None) -> Any:
        """Send a prompt to the LLM and get response"""
        pass
    
    @abstractmethod
    def handle_tool_call(self, tool_use: Dict, mcp_client) -> str:
        """Handle tool execution"""
        pass
