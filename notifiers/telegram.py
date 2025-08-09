import requests
from .base import Notifier

class TelegramNotifier(Notifier):
    """Telegram notification channel"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.thread_id = None
    
    def send_message(self, channel: str, message: str, create_thread=False, broadcast_final=False):
        """Send message to Telegram"""
        formatted = self.format_message(message)
        
        payload = {
            "chat_id": channel,
            "text": formatted,
            "parse_mode": "Markdown"
        }
        
        if self.thread_id and not create_thread:
            payload["reply_to_message_id"] = self.thread_id
        
        response = requests.post(f"{self.base_url}/sendMessage", json=payload)
        
        if response.status_code == 200 and create_thread:
            result = response.json()
            self.thread_id = result['result']['message_id']
    
    def format_message(self, message: str) -> str:
        """Format message for Telegram (supports Markdown)"""
        return message
