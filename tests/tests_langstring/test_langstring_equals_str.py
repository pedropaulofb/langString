import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "langstring_text, other_text, expected_result",
    [
        ("Hello", "Hello", True),
        ("hello", "Hello", False),
        ("", "", True),
        ("Test", "test", False),
        ("123", "123", True),
        ("Hello World", "hello world", False),
        ("Special chars !@#$%^&*", "Special chars !@#$%^&*", True),
        ("Multiline\ntext", "Multiline\ntext", True),
        ("Text with spaces    ", "Text with spaces    ", True),
        ("Text with tabs\t\t", "Text with tabs\t\t", True),
        (" Text with leading space", " Text with leading space", True),
        ("Text with trailing space ", "Text with trailing space ", True),
        ("   ", "   ", True),  # Strings with only spaces
        ("こんにちは", "こんにちは", True),  # Non-ASCII characters
        ("LongText" * 1000, "LongText" * 1000, True),  # Very long strings
        ("MixedCASE", "mixedcase", False),
        ("Line\nBreak", "Line\nBreak", True),
        ("Tabs\tand\nNewlines", "Tabs\tand\nNewlines", True),
    ],
)
def test_equals_str_various_cases(langstring_text: str, other_text: str, expected_result: bool) -> None:
    """
    Test the `equals_str` method for various cases including identical strings, case sensitivity,
    empty strings, numbers as strings, special characters, multiline texts, texts with spaces, and texts with tabs.

    :param langstring_text: The text to initialize LangString with.
    :param other_text: The string to compare against the LangString's text.
    :param expected_result: The expected result of the equality comparison.
    """
    lang_string = LangString(text=langstring_text, lang="en")
    assert (
        lang_string.equals_str(other_text) == expected_result
    ), f"Expected {expected_result} when comparing '{langstring_text}' with '{other_text}'"


@pytest.mark.parametrize("other_text", [123, True, None, set(), {}, 12.1, []])
def test_equals_str_invalid_type_other(other_text: str) -> None:
    """
    Test the `equals_str` method with invalid `other` parameter types to ensure type validation is effective.

    :param langstring_text: The text to initialize LangString with, assuming invalid types for `other`.
    :param other_text: The invalid type value to compare against the LangString's text.
    """
    lang_string = LangString(text="test", lang="en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        lang_string.equals_str(other_text)
