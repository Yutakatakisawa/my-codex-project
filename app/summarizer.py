"""A lightweight frequency-based text summarizer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


@dataclass
class SummaryResult:
    """Container for summarization output."""

    summary: str
    original_text: str


class FrequencySummarizer:
    """Summarize text by selecting the most informative sentences."""

    def __init__(self, language: str = "english", sentence_count: int = 3) -> None:
        self.language = language
        self.sentence_count = sentence_count
        try:
            self.stopwords = set(stopwords.words(language))
        except LookupError as exc:  # pragma: no cover - handled in tests
            raise RuntimeError(
                "NLTK stopwords not found. Run nltk.download('punkt') and nltk.download('stopwords')."
            ) from exc

    def summarize(self, text: str) -> SummaryResult:
        """Return the most relevant sentences from ``text``."""

        if not text.strip():
            raise ValueError("Cannot summarize empty text.")

        sentences = sent_tokenize(text)
        sentence_scores = self._score_sentences(sentences)
        ranked_sentences = sorted(
            sentence_scores,
            key=lambda item: item[1],
            reverse=True,
        )
        top_sentences = sorted(  # Keep original order
            (sentences.index(sentence), sentence)
            for sentence, _score in ranked_sentences[: self.sentence_count]
        )
        summary = " ".join(sentence for _idx, sentence in top_sentences)
        return SummaryResult(summary=summary, original_text=text)

    def _score_sentences(self, sentences: Iterable[str]) -> list[tuple[str, float]]:
        frequencies = self._word_frequencies(sentences)
        scores: list[tuple[str, float]] = []
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            sentence_words = [word for word in words if word.isalpha()]
            if not sentence_words:
                continue
            scores.append(
                (
                    sentence,
                    sum(frequencies.get(word, 0.0) for word in sentence_words)
                    / len(sentence_words),
                )
            )
        return scores

    def _word_frequencies(self, sentences: Iterable[str]) -> dict[str, float]:
        freq: dict[str, int] = {}
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            for word in words:
                if word.isalpha() and word not in self.stopwords:
                    freq[word] = freq.get(word, 0) + 1
        if not freq:
            return {}
        max_freq = max(freq.values())
        return {word: count / max_freq for word, count in freq.items()}


__all__ = ["SummaryResult", "FrequencySummarizer"]
