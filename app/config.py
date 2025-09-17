"""Configuration helpers for environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


class MissingConfigurationError(RuntimeError):
    """Raised when a required configuration value is missing."""


@dataclass
class OpenAIConfig:
    """Holds configuration for OpenAI API access."""

    api_key: str
    model: str = "gpt-4o-mini-transcribe"

    @classmethod
    def load(cls) -> "OpenAIConfig":
        """Load configuration values from the environment."""

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise MissingConfigurationError(
                "OPENAI_API_KEY must be set to use the transcription service."
            )
        model = os.getenv("OPENAI_TRANSCRIBE_MODEL", cls.model)
        return cls(api_key=api_key, model=model)


@dataclass
class LineConfig:
    """Holds configuration for LINE Messaging API access."""

    channel_access_token: str

    @classmethod
    def load(cls) -> "LineConfig":
        """Load LINE configuration from the environment."""

        token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        if not token:
            raise MissingConfigurationError(
                "LINE_CHANNEL_ACCESS_TOKEN must be set to send messages."
            )
        return cls(channel_access_token=token)
