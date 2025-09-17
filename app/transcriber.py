"""Transcription utilities using the OpenAI API."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

import openai

from .config import OpenAIConfig


class TranscriptionResult(dict):
    """Dictionary subclass giving attribute access to transcription data."""

    @property
    def text(self) -> str:
        return self["text"]


class Transcriber(Protocol):
    """Protocol describing objects capable of transcribing audio."""

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        ...


class OpenAIWhisperTranscriber:
    """Transcribes audio using OpenAI's Whisper API."""

    def __init__(self, config: OpenAIConfig | None = None) -> None:
        self.config = config or OpenAIConfig.load()
        openai.api_key = self.config.api_key

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """Send the audio file to OpenAI and return the transcription result."""

        with audio_path.open("rb") as audio_file:
            response = openai.audio.transcriptions.create(
                file=audio_file,
                model=self.config.model,
                response_format="json",
            )
        text = response.text if hasattr(response, "text") else response["text"]
        return TranscriptionResult(text=text)


__all__ = ["TranscriptionResult", "Transcriber", "OpenAIWhisperTranscriber"]
