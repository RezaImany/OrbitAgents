import os
import re
from slack_sdk import WebClient

class slack:
    def __init__(self,token):
        self.token = token
        self.thread_ts = None
    
    def md_to_mrkdwn(self,md: str) -> str:
        s = md.replace("\r\n", "\n")

        # --- Headings ---
        # H1 (# ...) -> uppercase bold + divider
        s = re.sub(r"^# (.+)$", lambda m: f"*{m.group(1).upper()}*\n{'─'*30}", s, flags=re.M)
        # H2 (## ...) -> bold
        s = re.sub(r"^## (.+)$", lambda m: f"*{m.group(1).strip()}*", s, flags=re.M)
        # H3 (### ...) -> italic
        s = re.sub(r"^### (.+)$", lambda m: f"_{m.group(1).strip()}_", s, flags=re.M)

        # --- Bold / Italic ---
        s = re.sub(r"\*\*(.+?)\*\*", r"*\1*", s)    # **bold** → *bold*
        s = re.sub(r"_(.+?)_", r"_\1_", s)          # _italic_ → _italic_

        # --- Lists ---
        s = re.sub(r"^- (.+)$", r"• \1", s, flags=re.M)

        return s

    def send_message(self,channel, message, create_thread=False, broadcast_final=False):
        slack_client = WebClient(token=self.token)
        message = self.md_to_mrkdwn(message)
        
        if create_thread or self.thread_ts is None:
            response = slack_client.chat_postMessage(
                channel=channel,
                text=message
            )
            self.thread_ts = response['ts']
        else:
            slack_client.chat_postMessage(
                channel=channel,
                text=message,
                thread_ts=self.thread_ts,
                reply_broadcast=broadcast_final
            )

