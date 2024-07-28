import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_lang, expected_result",
    [
        ("en", True),  # Basic positive case
        ("EN", True),  # Case-insensitive check
        (" en ", False),  # Leading and trailing spaces
        ("es", True),  # Another positive case with a different language
        ("es-ES", True),  # Language code with region
        ("Ελ", False),  # Greek characters, not present
        ("Привет", False),  # Cyrillic characters, not present
        ("😀", False),  # Emoji, not present
        (" special ", False),  # Special characters with spaces, not present
        ("", False),  # Empty string, adjusted type
        ("🚀", False),  # Emoji as input
        ("   ", False),  # Spaces only as input
    ],
)
def test_multilangstring_contains_positive(input_lang, expected_result):
    """Test the __contains__ method in MultiLangString for positive scenarios.

    :param input_lang: The language code to check in the MultiLangString instance.
    :param expected_result: The expected boolean result indicating presence of the language code.
    """
    mls = MultiLangString(
        mls_dict={
            "en": {"Hello World"},
            " es ": {"Hola Mundo"},
            "es": {"Hola Mundo"},
            "es-ES": {"Hola Mundo"},
        }
    )
    assert (input_lang in mls) == expected_result, f"Expected {input_lang} in mls to be {expected_result}"


@pytest.mark.parametrize(
    "input_lang, expected_exception",
    [
        (None, TypeError),  # Non-string input
        (123, TypeError),  # Non-string input
        ([], TypeError),  # List as input
        ({}, TypeError),  # Dict as input
    ],
)
def test_multilangstring_contains_negative(input_lang, expected_exception):
    """Test the __contains__ method in MultiLangString for negative scenarios, expecting exceptions.

    :param input_lang: The language code (or invalid input) to check in the MultiLangString instance.
    :param expected_exception: The type of exception expected to be raised.
    :param match_msg: The expected message in the exception.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello World"}})
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        assert input_lang in mls


@pytest.mark.parametrize(
    "input_lang, expected_result",
    [
        ("", True),  # Empty language code
        ("und", True),  # Undetermined language code
        ("EN ", False),  # Language code with trailing space, considered present
        (" es-ES", False),  # Language code with leading space and region, considered present
    ],
)
def test_multilangstring_contains_edge_cases(input_lang, expected_result):
    """Test __contains__ for edge cases including default, null, and unusual but valid inputs."""
    mls = MultiLangString(mls_dict={"": {"Empty"}, "und": {"Undetermined"}})
    assert (input_lang in mls) == expected_result, f"Edge case {input_lang} not handled as expected."


def test_multilangstring_operation_on_itself():
    """Test operations on itself to ensure stability and expected behavior."""
    mls_instance = MultiLangString(mls_dict={"en": {"Hello World"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls_instance in mls_instance
