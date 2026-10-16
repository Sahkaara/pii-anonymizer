# src/pii_anonymizer/core.py
import re

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize the Presidio Analyzer and Anonymizer engines.
# These are instantiated once at module level so the underlying NLP models
# are loaded only a single time, avoiding a heavy overhead on every call.
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


# Mapping between detected PII entity types and the anonymization operator
# to apply. Each entity can be handled with a different strategy:
#   - "replace": substitute the PII with a fixed placeholder (default behavior)
#   - "mask":    keep the original length but hide characters with a masking char
#   - "redact":  completely remove the PII from the text
#   - "hash":    replace the PII with a cryptographic hash (pseudonymization)
#   - "encrypt": encrypt the PII so it can be reversed with a key (pseudonymization)
OPERATORS = {
    "PERSON": OperatorConfig("replace", {"new_value": "[NAME]"}),
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
    "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
    "CREDIT_CARD": OperatorConfig(
        "mask",
        {"masking_char": "*", "chars_to_mask": 12, "from_end": False},
    ),
    "US_SSN": OperatorConfig("redact"),
    "IP_ADDRESS": OperatorConfig("replace", {"new_value": "[IP_ADDRESS]"}),
    "DATE_TIME": OperatorConfig("replace", {"new_value": "[DATE_TIME]"}),
    "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATION]"}),
    "URL": OperatorConfig("replace", {"new_value": "[URL]"}),
    "US_BANK_NUMBER": OperatorConfig(
        "mask",
        {"masking_char": "*", "chars_to_mask": 12, "from_end": False},
    ),
    "US_DRIVER_LICENSE": OperatorConfig("replace", {"new_value": "[DRIVER_LICENSE]"}),
    "US_PASSPORT": OperatorConfig("replace", {"new_value": "[PASSPORT]"}),
    "US_ITIN": OperatorConfig("replace", {"new_value": "[ITIN]"}),
    "US_NATIONAL_ID": OperatorConfig("replace", {"new_value": "[NATIONAL_ID]"}),
    "US_VISA": OperatorConfig("replace", {"new_value": "[VISA]"}),
    # Additional entities detected by Presidio's default recognizers.
    # Without these, the tool falls back to a generic <ENTITY_TYPE> placeholder.
    "NRP": OperatorConfig("replace", {"new_value": "[NAZIONALITA]"}),
    "UK_NHS": OperatorConfig("replace", {"new_value": "[PHONE]"}),
}


# Regex used to restore newlines that Presidio's PERSON recognizer sometimes
# swallows when replacing a name. It matches a placeholder immediately followed
# by an uppercase letter, e.g. "[NAME]Date of Birth" -> "[NAME]\nDate of Birth".
_MISSING_NEWLINE_PATTERN = re.compile(r"(\[[A-Z_]+\])(?=[A-Z])")


def anonymize_text(text: str, language: str = "en") -> str:
    """
    Detect and anonymize personally identifiable information (PII) in text.

    Args:
        text (str): The input text containing potential PII.
        language (str): The language of the input text. Default is "en" (English).

    Returns:
        str: The anonymized text with PII replaced by placeholders.

    Raises:
        ValueError: If the requested language is not supported by the analyzer.
    """
    # Short-circuit on empty or whitespace-only input to avoid useless work.
    if not text or not text.strip():
        return text

    # Fail fast if the user asks for a language the analyzer doesn't know about.
    # This produces a clean error message instead of a cryptic Presidio traceback.
    if language not in analyzer.supported_languages:
        raise ValueError(
            f"Language '{language}' is not supported. "
            f"Available languages: {analyzer.supported_languages}"
        )

    # Detect PII entities in the text.
    # The analyzer returns a list of RecognizerResult objects, each one
    # describing the entity type, its position (start/end) and a confidence score.
    results = analyzer.analyze(text=text, language=language)

    # Apply the configured operators to the detected entities.
    # Any entity type not listed in OPERATORS falls back to the default
    # "replace" operator with a generic "<ENTITY_TYPE>" placeholder.
    anonymized_results = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=OPERATORS,
    )

    # Post-processing: Presidio's PERSON recognizer sometimes includes the
    # trailing newline in its match. When the name is replaced, that newline
    # is lost, gluing the placeholder to the next line's content. This step
    # restores a newline when a placeholder is immediately followed by an
    # uppercase letter.
    cleaned = _MISSING_NEWLINE_PATTERN.sub(r"\1\n", anonymized_results.text)

    return cleaned