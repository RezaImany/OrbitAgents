import re
from slack_sdk import WebClient
from .base import Notifier

class SlackNotifier(Notifier):
    """Slack notification channel"""
    
    def __init__(self, token: str):
        self.token = token
        self.client = WebClient(token=token)
        self.thread_ts = None
    
    def send_message(self, channel: str, message: str, create_thread=False, broadcast_final=False):
        """Send message to Slack"""
        formatted = self.format_message(message)
        
        if create_thread or self.thread_ts is None:
            response = self.client.chat_postMessage(
                channel=channel,
                text=formatted
            )
            self.thread_ts = response['ts']
        else:
            self.client.chat_postMessage(
                channel=channel,
                text=formatted,
                thread_ts=self.thread_ts,
                reply_broadcast=broadcast_final
            )
    
    def format_message(self, message: str) -> str:
        """Convert markdown to Slack mrkdwn"""
        s = message.replace("\r\n", "\n")
        s = re.sub(r"^# (.+)$", lambda m: f"*{m.group(1).upper()}*\n{'─'*30}", s, flags=re.M)
        s = re.sub(r"^## (.+)$", lambda m: f"*{m.group(1).strip()}*", s, flags=re.M)
        s = re.sub(r"^### (.+)$", lambda m: f"_{m.group(1).strip()}_", s, flags=re.M)
        s = re.sub(r"\*\*(.+?)\*\*", r"*\1*", s)
        s = re.sub(r"^- (.+)$", r"• \1", s, flags=re.M)
        return s
