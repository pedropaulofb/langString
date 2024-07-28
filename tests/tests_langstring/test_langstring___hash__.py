import pytest
from langstring import LangString

# Test cases for __hash__ method
hash_test_cases = [
    ("hello", "en"),
    ("こんにちは", "ja"),  # Unicode characters
    ("hello", "EN"),  # Different case in lang
    ("hello", "en"),  # Same text and lang
    ("hello", "fr"),  # Different lang
    ("world", "en"),  # Different text
    ("", "en"),  # Empty text
    ("hello", ""),  # Empty lang
    ("", ""),  # Empty text and lang
    (" ", " "),  # Space text and lang
    (" hello", "en"),
    ("hello ", "en"),
    ("hello", " en"),
    ("hello", "en "),
    ("Hello", "en"),  # Different text case
    ("hello", "EN-GB"),  # Different lang case and format
    ("world", "fr"),  # Different text and lang
    ("123", "en"),  # Numeric text
    ("hello world", "en"),  # Text with space
    (" hello ", "en"),  # Text with leading/trailing spaces
    ("special&*chars", "en"),  # Special characters
    ("こんにちは", "ja"),  # Unicode, different lang
    ("longtext" * 10, "en"),  # Long text
    ("multi\nline", "en"),  # Multiline text
]


@pytest.mark.parametrize("text, lang", hash_test_cases)
def test_hash_method(text: str, lang: str) -> None:
    """
    Test the __hash__ method of LangString.

    :param text: The text of the LangString.
    :param lang: The language tag of the LangString.
    """
    lang_string = LangString(text, lang)
    expected_hash = hash((text, lang.casefold()))
    assert hash(lang_string) == expected_hash, f"Hash mismatch for LangString with text '{text}' and lang '{lang}'"


@pytest.mark.parametrize("text, lang", hash_test_cases)
def test_hash_consistency(text: str, lang: str) -> None:
    """
    Test the consistency of hash values for the same LangString instance.
    """
    lang_string = LangString(text, lang)
    first_hash = hash(lang_string)
    second_hash = hash(lang_string)
    assert first_hash == second_hash, "Hash values should be consistent across multiple calls"


def test_hash_uniqueness() -> None:
    """
    Test the uniqueness of hash values for different LangString instances,
    considering case-insensitive language tags.
    """
    unique_hash_test_cases = [
        ("hello", "en"),
        ("hello", "fr"),
        ("world", "en"),
        ("unique1", "en"),
        ("unique2", "fr"),
        ("unique3", "es"),
        ("特別な", "ja"),  # Unique unicode text
        ("longunique" * 10, "en"),  # Long unique text
        ("unique&*chars", "en"),  # Unique special characters
        ("unique", "en-US"),  # Complex language tag
        ("unique", "en-GB"),  # Different complex language tag
    ]

    lang_strings = [LangString(text, lang) for text, lang in unique_hash_test_cases]
    hashes = set(hash(ls) for ls in lang_strings)
    assert len(hashes) == len(unique_hash_test_cases), "Hash values should be unique for different LangString instances"
