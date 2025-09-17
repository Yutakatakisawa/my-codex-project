"""LINE Messaging API client."""

from __future__ import annotations

from dataclasses import dataclass

from linebot import LineBotApi
from linebot.models import TextSendMessage

from .config import LineConfig


@dataclass
class LineMessenger:
    """Send text messages to a LINE user or group."""

    line_api: LineBotApi

    @classmethod
    def from_config(cls, config: LineConfig | None = None) -> "LineMessenger":
        config = config or LineConfig.load()
        return cls(line_api=LineBotApi(config.channel_access_token))

    def send_text(self, user_id: str, message: str) -> None:
        """Send ``message`` to the specified ``user_id``."""

        if not message.strip():
            raise ValueError("Cannot send an empty message to LINE.")
        self.line_api.push_message(user_id, TextSendMessage(text=message))


__all__ = ["LineMessenger"]
