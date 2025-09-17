"""Command line interface for recording, summarizing, and sending to LINE."""

from __future__ import annotations

import argparse

from .line_client import LineMessenger
from .recorder import AudioRecorder
from .summarizer import FrequencySummarizer
from .transcriber import OpenAIWhisperTranscriber


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record audio, summarize it, and send the summary via LINE.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=15.0,
        help="Recording duration in seconds (default: 15).",
    )
    parser.add_argument(
        "--line-user-id",
        required=True,
        help="Destination LINE user ID for the summary message.",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep the recorded audio file instead of deleting it.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    recorder = AudioRecorder()
    transcriber = OpenAIWhisperTranscriber()
    summarizer = FrequencySummarizer()
    line_messenger = LineMessenger.from_config()

    audio_path = recorder.record(args.duration)
    try:
        transcription = transcriber.transcribe(audio_path)
        summary = summarizer.summarize(transcription.text)
        line_messenger.send_text(args.line_user_id, summary.summary)
        print("Summary sent to LINE user", args.line_user_id)
        print("Summary:\n", summary.summary)
    finally:
        if not args.keep_audio:
            try:
                audio_path.unlink()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    main()
