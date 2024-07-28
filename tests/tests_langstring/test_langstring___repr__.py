import pytest
from langstring import LangString

# Test cases for __repr__ method
repr_test_cases = [
    ("hello", "en"),
    ("こんにちは", "ja"),  # Unicode characters
    ("", ""),  # Empty text and lang
    ("😊", "emoji"),  # Emoji in text
    ("hello\nworld", "en"),  # Multiline text
    ("hello", "EN"),  # Different case in lang
    (" " * 10, "whitespace"),  # Whitespace in text
    ("special'chars", "en"),  # Special characters in text
    ("long" * 100, "en"),  # Long text
    ("12345", "num"),  # Numeric text
    ("True", "bool"),  # Boolean-like text
    ("None", "none"),  # None-like text
    ("hello" * 1000, "long"),  # Extremely long text
    ("new\nline\ncharacters", "multi-line"),  # Text with new line characters
    ("tab\tcharacters", "tab"),  # Text with tab characters
    ("", "en"),  # Empty text with valid lang
    ("hello", ""),  # Valid text with empty lang
    (" ", " "),  # Single space in text and lang
    ("mixedCASE", "MiXeD"),  # Mixed case in text and lang
]


@pytest.mark.parametrize("text, lang", repr_test_cases)
def test_repr_method(text: str, lang: str) -> None:
    """
    Test the __repr__ method of LangString.

    :param text: The text of the LangString.
    :param lang: The language tag of the LangString.
    """
    lang_string = LangString(text, lang)
    expected_repr = f"LangString(text={repr(text)}, lang={repr(lang)})"
    assert repr(lang_string) == expected_repr, f"__repr__ failed for LangString with text '{text}' and lang '{lang}'"
