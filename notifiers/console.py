from .base import Notifier

class ConsoleNotifier(Notifier):
    """Console/stdout notification channel (for testing)"""
    
    def __init__(self):
        pass
    
    def send_message(self, channel: str, message: str, **kwargs):
        """Print message to console"""
        formatted = self.format_message(message)
        print(f"[{channel}] {formatted}")
    
    def format_message(self, message: str) -> str:
        """No formatting needed for console"""
        return message
