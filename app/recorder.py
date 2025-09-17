"""Audio recording utilities using the sounddevice library."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

import sounddevice as sd
from scipy.io import wavfile


class AudioRecorder:
    """Handles recording audio from the system microphone."""

    def __init__(self, sample_rate: int = 16_000, channels: int = 1) -> None:
        self.sample_rate = sample_rate
        self.channels = channels

    def record(self, duration: float, output_path: Optional[Path] = None) -> Path:
        """Record audio for ``duration`` seconds and save it as a WAV file."""

        if duration <= 0:
            raise ValueError("Duration must be positive.")

        output_path = output_path or Path(tempfile.mkstemp(suffix=".wav")[1])
        num_samples = int(duration * self.sample_rate)
        recording = sd.rec(
            frames=num_samples,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
        )
        sd.wait()
        wavfile.write(output_path, self.sample_rate, recording)
        return output_path


__all__ = ["AudioRecorder"]
