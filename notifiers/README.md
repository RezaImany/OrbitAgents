# Notifiers

This directory contains notification channel implementations. Each notifier is a self-contained class that handles sending messages to a specific platform.

## Available Notifiers

- **SlackNotifier** - Slack channels
- **TelegramNotifier** - Telegram chats
- **ConsoleNotifier** - Console output (for testing)

## Creating a New Notifier

1. Create a new file: `notifiers/your_notifier.py`
2. Inherit from `Notifier` base class
3. Implement required methods:
   - `send_message(channel, message, **kwargs)` - Send notification
   - `format_message(message)` - Format message for platform

### Example Template

```python
from .base import Notifier

class YourNotifier(Notifier):
    """Your notifier description"""
    
    def __init__(self, **kwargs):
        """
        Initialize notifier
        
        Args:
            **kwargs: Notifier-specific configuration (tokens, URLs, etc.)
        """
        # Your initialization
        pass
    
    def send_message(self, channel: str, message: str, **kwargs):
        """
        Send message to notification channel
        
        Args:
            channel: Target channel/chat/recipient
            message: Message content
            **kwargs: Additional options (create_thread, broadcast_final, etc.)
        """
        formatted = self.format_message(message)
        # Your implementation
    
    def format_message(self, message: str) -> str:
        """
        Format message for platform
        
        Args:
            message: Raw message (may contain markdown)
            
        Returns:
            Formatted message for platform
        """
        # Your implementation
        return message
```

4. Add to `notifiers/__init__.py`:
```python
from .your_notifier import YourNotifier
__all__ = [..., 'YourNotifier']
```

5. Document environment variables in `.env.example`

## Environment Variables

Each notifier should document its required environment variables:

### Slack
```env
SLACK_TOKEN=xoxb-your-token
SLACK_CHANNEL=#your-channel
```

### Telegram
```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

### Console
No configuration needed.

## Notifier Configuration

Notifiers are configured in `notifiers/factory.py` which handles instantiation based on environment variables.
