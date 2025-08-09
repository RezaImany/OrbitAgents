"""
Notifier Factory

Handles instantiation of notifiers based on configuration.
Add new notifiers here to make them available via environment variables.
"""

import os
from .slack import SlackNotifier
from .telegram import TelegramNotifier
from .console import ConsoleNotifier

# Registry of available notifiers
NOTIFIERS = {
    'slack': {
        'class': SlackNotifier,
        'config': lambda: {
            'token': os.getenv('SLACK_TOKEN')
        },
        'channel': lambda: os.getenv('SLACK_CHANNEL', '#general')
    },
    'telegram': {
        'class': TelegramNotifier,
        'config': lambda: {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN')
        },
        'channel': lambda: os.getenv('TELEGRAM_CHAT_ID')
    },
    'console': {
        'class': ConsoleNotifier,
        'config': lambda: {},
        'channel': lambda: 'console'
    },
    # Add new notifiers here:
    # 'your_notifier': {
    #     'class': YourNotifier,
    #     'config': lambda: {
    #         'api_key': os.getenv('YOUR_NOTIFIER_API_KEY'),
    #         # ... other config
    #     },
    #     'channel': lambda: os.getenv('YOUR_NOTIFIER_CHANNEL')
    # }
}

def create_notifier(notifier_type: str = None):
    """
    Create notifier instance based on configuration
    
    Args:
        notifier_type: Notifier type (slack, telegram, console, etc.)
                      If None, reads from NOTIFIER env var
    
    Returns:
        Tuple of (notifier_instance, default_channel)
        
    Raises:
        ValueError: If notifier type is unsupported or configuration is invalid
    """
    notifier_type = notifier_type or os.getenv('NOTIFIER', 'console').lower()
    
    if notifier_type not in NOTIFIERS:
        available = ', '.join(NOTIFIERS.keys())
        raise ValueError(
            f"Unsupported notifier: '{notifier_type}'. "
            f"Available notifiers: {available}"
        )
    
    notifier_info = NOTIFIERS[notifier_type]
    config = notifier_info['config']()
    channel = notifier_info['channel']()
    
    # Validate required configuration (skip console which needs no config)
    if notifier_type != 'console' and not all(config.values()):
        missing = [k for k, v in config.items() if not v]
        raise ValueError(
            f"Missing configuration for {notifier_type}: {', '.join(missing)}"
        )
    
    notifier = notifier_info['class'](**config)
    return notifier, channel

def list_notifiers():
    """List all available notifier types"""
    return list(NOTIFIERS.keys())
