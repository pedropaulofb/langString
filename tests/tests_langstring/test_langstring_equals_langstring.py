import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "text1, lang1, text2, lang2, expected_result",
    [
        ("Hello", "en", "Hello", "en", True),
        ("hello", "en", "Hello", "en", False),
        ("", "en", "", "en", True),
        ("Test", "en", "test", "en", False),
        ("123", "en", "123", "en", True),
        ("Hello World", "en", "hello world", "en", False),
        ("hello", "EN", "hello", "en", True),
        ("hello", "en", "hello", "EN", True),
        ("hello", "en_us", "hello", "en_gb", False),
        ("こんにちは", "jp", "こんにちは", "jp", True),
        ("hello", "en", "hello", "fr", False),
        ("LongText" * 1000, "en", "LongText" * 1000, "en", True),
        ("Text with spaces    ", "en", "Text with spaces    ", "en", True),
        ("Text", "en", "Text", "", False),
        ("", "", "", "", True),
    ],
)
def test_equals_langstring_various_cases(text1: str, lang1: str, text2: str, lang2: str, expected_result: bool) -> None:
    """
    Test the `equals_langstring` method for various cases including identical strings with same languages, case
    sensitivity, empty strings, strings with different languages, non-ASCII characters, very long strings, and
    strings with trailing spaces.

    :param text1: The text of the first LangString object.
    :param lang1: The language of the first LangString object.
    :param text2: The text of the second LangString object to compare against.
    :param lang2: The language of the second LangString object to compare against.
    :param expected_result: The expected result of the equality comparison.
    """
    lang_string1 = LangString(text=text1, lang=lang1)
    lang_string2 = LangString(text=text2, lang=lang2)
    assert (
        lang_string1.equals_langstring(lang_string2) == expected_result
    ), f"Expected {expected_result} when comparing LangString('{text1}', '{lang1}') with LangString('{text2}', '{lang2}')"


@pytest.mark.parametrize("invalid_type", [123, True, None, set(), {}, 12.1, []])
def test_equals_langstring_invalid_type(invalid_type) -> None:
    """
    Test the `equals_langstring` method with invalid input types to ensure type validation is enforced.

    :param invalid_type: An invalid input type to test against the LangString's equals_langstring method.
    """
    lang_string = LangString(text="test", lang="en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        lang_string.equals_langstring(invalid_type)
