from __future__ import annotations

import nltk
import pytest

from app.summarizer import FrequencySummarizer


def setup_module(module):
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    nltk.download("stopwords", quiet=True)


def test_summarizer_returns_sentences():
    text = (
        "Python is a programming language that lets you work quickly. "
        "Python has simple syntax and a large community. "
        "It is widely used for scripting, data science, and web development."
    )
    summarizer = FrequencySummarizer(sentence_count=2)
    result = summarizer.summarize(text)
    assert result.summary
    assert result.original_text == text
    assert result.summary.count(".") >= 1


def test_empty_text_raises_value_error():
    summarizer = FrequencySummarizer()
    with pytest.raises(ValueError):
        summarizer.summarize("   ")
