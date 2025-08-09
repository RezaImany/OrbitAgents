from abc import ABC, abstractmethod

class Notifier(ABC):
    """Base class for notification channels"""
    
    @abstractmethod
    def send_message(self, channel: str, message: str, **kwargs):
        """Send a message to the notification channel"""
        pass
    
    @abstractmethod
    def format_message(self, message: str) -> str:
        """Format message for the specific channel"""
        pass
