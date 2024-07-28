import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello", True),  # Text present in one of the languages
        ("Hola", True),  # Text present in another language
        ("Bonjour", False),  # Text not present in any language
        ("hello", False),  # Case sensitivity check
        ("", False),  # Empty text string
    ],
)
def test_contains_text_in_any_lang_valid_input(text: str, expected: bool):
    """
    Test `contains_text_in_any_lang` method with valid input text.

    :param text: The text to search across all languages.
    :param expected: The expected boolean outcome.
    :return: Asserts if `contains_text_in_any_lang` correctly identifies the presence or absence of text.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "es": {"Hola"}})
    assert (
        mls.contains_text_in_any_lang(text) == expected
    ), f"contains_text_in_any_lang('{text}') should return {expected}"


@pytest.mark.parametrize(
    "text",
    [
        (123),  # Integer
        (None),  # None
        ([],),  # List
        ({},),  # Dictionary
    ],
)
def test_contains_text_in_any_lang_invalid_input_type(text):
    """
    Test `contains_text_in_any_lang` method with invalid input types for text.

    :param text: The invalid text input to test.
    :raises TypeError: If `text` is not a string.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.contains_text_in_any_lang(text)


@pytest.mark.parametrize(
    "flag, text, expected",
    [
        (
            MultiLangStringFlag.LOWERCASE_LANG,
            "hello",
            True,
        ),  # LOWERCASE_LANG flag effect, assuming case-insensitive search
    ],
)
def test_contains_text_in_any_lang_with_flag_effect(flag: MultiLangStringFlag, text: str, expected: bool):
    """
    Test `contains_text_in_any_lang` considering the effect of MultiLangString flags.

    :param flag: The flag to test the effect of.
    :param text: The text to search for across all languages.
    :param expected: The expected outcome of the contains_text_in_any_lang call.
    """
    Controller.set_flag(flag, True)
    mls = MultiLangString(mls_dict={"en": {"hello"}, "es": {"hola"}})
    assert (
        mls.contains_text_in_any_lang(text) == expected
    ), f"With '{flag}' flag, contains_text_in_any_lang('{text}') should return {expected}"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("こんにちは", True),  # Non-Latin script (Japanese for "Hello")
        ("👋", False),  # Emoji not present
        ("Hel", False),  # Substring of an existing text
        ("lo", False),  # Another substring
        ("Quetzalcoatl", False),  # Uncommon and not present
    ],
)
def test_contains_text_in_any_lang_unusual_but_valid_usage(text: str, expected: bool):
    """
    Test `contains_text_in_any_lang` for unusual but valid usage scenarios.

    :param text: The text to search across all languages.
    :param expected: The expected boolean outcome.
    :return: Asserts if `contains_text_in_any_lang` behaves as expected even in unusual scenarios.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello", "Hello there"}, "jp": {"こんにちは"}})
    assert mls.contains_text_in_any_lang(text) == expected, f"Unusual but valid text '{text}' should return {expected}"
