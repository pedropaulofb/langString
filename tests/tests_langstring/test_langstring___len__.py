import pytest
from langstring import LangString

# Test cases for __len__ method
len_test_cases = [
    ("hello", len("hello")),
    ("", len("")),  # Empty string
    (" ", len(" ")),  # Single space
    ("こんにちは", len("こんにちは")),  # Unicode characters
    ("hello world", len("hello world")),  # Text with space
    ("longtext" * 100, len("longtext" * 100)),  # Long text
    ("\n\t", len("\n\t")),  # Special whitespace characters
    ("multi\nline", len("multi\nline")),  # Multiline text
    ("😊", len("😊")),  # Single emoji (unicode character)
    ("😊😊😊", len("😊😊😊")),  # Multiple emojis
    ("    ", len("    ")),  # String with only spaces
]


@pytest.mark.parametrize("text, expected_length", len_test_cases)
def test_len_method(text: str, expected_length: int) -> None:
    """
    Test the __len__ method of LangString.

    :param text: The text of the LangString.
    :param expected_length: The expected length of the text.
    """
    lang_string = LangString(text, "en")
    assert len(lang_string) == expected_length, f"Length mismatch for LangString with text '{text}'"


def test_len_consistency() -> None:
    """
    Test the consistency of length values for the same LangString instance.
    """
    lang_string = LangString("consistent length", "en")
    first_len = len(lang_string)
    second_len = len(lang_string)
    assert first_len == second_len, "Length values should be consistent across multiple calls"
