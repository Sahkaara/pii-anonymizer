# tests/test_core.py
import pytest

from pii_anonymizer.core import anonymize_text


def test_anonymize_person_and_email():
    """A person name and an email address should be replaced by placeholders."""
    text = "Hi, my name is John Smith and my email is john.smith@example.com."
    result = anonymize_text(text, language="en")

    assert "John Smith" not in result
    assert "john.smith@example.com" not in result
    assert "[NAME]" in result
    assert "[EMAIL]" in result


def test_anonymize_phone_number():
    """A US-style phone number should be detected and replaced."""
    text = "Call me at 212-555-1234 when you're free."
    result = anonymize_text(text, language="en")

    assert "212-555-1234" not in result
    assert "[PHONE]" in result


def test_anonymize_credit_card_is_masked():
    """A credit card number should be masked, not fully replaced."""
    text = "My card number is 4095-2609-9393-4932."
    result = anonymize_text(text, language="en")

    # The original digits must not appear verbatim in the output.
    assert "4095-2609-9393-4932" not in result
    # The mask operator keeps the shape of the value: some digits remain visible.
    assert "*" in result


def test_anonymize_empty_text_returns_empty():
    """An empty or whitespace-only input should be returned unchanged."""
    assert anonymize_text("", language="en") == ""
    assert anonymize_text("   \n\t ", language="en") == "   \n\t "


def test_anonymize_text_without_pii_is_unchanged():
    """A text with no PII should pass through with no substitutions."""
    text = "The quick brown fox jumps over the lazy dog."
    result = anonymize_text(text, language="en")

    assert result == text


def test_unsupported_language_raises_value_error():
    """Requesting a language the analyzer doesn't support must raise ValueError."""
    with pytest.raises(ValueError):
        anonymize_text("Hello world", language="xx")