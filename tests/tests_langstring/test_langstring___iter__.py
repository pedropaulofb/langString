import pytest
from langstring import LangString

# Test cases for __iter__ method
iter_test_cases = [
    ("hello", list("hello")),
    ("", list("")),  # Empty string
    (" ", list(" ")),  # Single space
    ("こんにちは", list("こんにちは")),  # Unicode characters
    ("hello world", list("hello world")),  # Text with space
    ("\n\t", list("\n\t")),  # Special whitespace characters
    ("😊", list("😊")),  # Single emoji (unicode character)
    ("😊😊😊", list("😊😊😊")),  # Multiple emojis
]


@pytest.mark.parametrize("text, expected_iter", iter_test_cases)
def test_iter_method(text: str, expected_iter: list[str]) -> None:
    """
    Test the __iter__ method of LangString.

    :param text: The text of the LangString.
    :param expected_iter: The expected list of characters from iterating over the text.
    """
    lang_string = LangString(text, "en")
    assert list(iter(lang_string)) == expected_iter, f"Iteration mismatch for LangString with text '{text}'"


def test_iter_consistency() -> None:
    """
    Test the consistency of iteration for the same LangString instance.
    """
    lang_string = LangString("consistent iteration", "en")
    first_iter = list(iter(lang_string))
    second_iter = list(iter(lang_string))
    assert first_iter == second_iter, "Iteration results should be consistent across multiple calls"
