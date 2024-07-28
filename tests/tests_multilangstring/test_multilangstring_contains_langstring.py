import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangString
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "text, lang, expected",
    [
        ("Hello", "en", True),  # Case where the language string exists
        ("Hello", "EN", True),  # Test LOWERCASE_LANG effect
        ("Hola", "es", True),  # Another language
        ("Bonjour", "fr", False),  # Language string does not exist
        ("Hello World", "en", False),  # Case with space in text
        ("こんにちは", "jp", True),  # Non-Latin script
        ("", "en", False),  # Empty text string
        ("Hello", "", False),  # Empty language code
    ],
)
def test_contains_langstring_valid_input(text: str, lang: str, expected: bool):
    """
    Test contains_langstring with valid input.

    :param text: The text to be checked.
    :param lang: The language of the text.
    :param expected: Expected result (True if exists, False otherwise).
    """
    langstring = LangString(text, lang)
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "es": {"Hola"}, "jp": {"こんにちは"}})
    assert (
        mls.contains_langstring(langstring) == expected
    ), f"Expected {expected} for text '{text}' in language '{lang}'"


@pytest.mark.parametrize(
    "text, lang",
    [
        (123, "en"),  # Invalid text type
        ("Hello", 456),  # Invalid lang type
        ([], "en"),  # List as text
        ("Hello", []),  # List as language
    ],
)
def test_contains_langstring_invalid_input_types(text: str, lang: str):
    """
    Test contains_langstring with invalid input types.

    :param text: The text to be checked, intentionally the wrong type.
    :param lang: The language of the text, intentionally the wrong type.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        langstring = LangString(text, lang)
        mls = MultiLangString()
        mls.contains_langstring(langstring)


def test_contains_langstring_empty_mls():
    """
    Test contains_langstring with an empty MultiLangString.
    """
    langstring = LangString("Hello", "en")
    mls = MultiLangString()
    assert not mls.contains_langstring(langstring), "Expected False for an empty MultiLangString"


def test_contains_langstring_no_lang():
    """
    Test contains_langstring with a LangString in a language not present in MultiLangString.
    """
    langstring = LangString("Hello", "de")  # 'de' language not in MLS
    mls = MultiLangString(mls_dict={"en": {"Hello"}})
    assert not mls.contains_langstring(langstring), "Expected False when language is not present in MultiLangString"


@pytest.mark.parametrize(
    "flag, flag_state, text, lang, expected",
    [
        (MultiLangStringFlag.VALID_LANG, True, "Hello", "en", True),  # Flag affects validation
        (GlobalFlag.LOWERCASE_LANG, True, "HELLO", "EN", False),  # Global flag affects all lang strings
        (
            MultiLangStringFlag.DEFINED_TEXT,
            False,
            "",
            "en",
            False,
        ),  # Text field non-mandatory, but empty text not in MLS
    ],
)
def test_contains_langstring_with_flags_effect(flag, flag_state, text, lang, expected):
    """
    Test contains_langstring considering the effect of flags.

    :param flag: The flag to be tested.
    :param flag_state: The state (True/False) to set for the flag.
    :param text: The text of the LangString.
    :param lang: The language code of the LangString.
    :param expected: The expected result of the contains_langstring call.
    """
    Controller.set_flag(flag, flag_state)
    langstring = LangString(text, lang)
    mls = MultiLangString(mls_dict={"en": {"Hello"}})
    assert (
        mls.contains_langstring(langstring) == expected
    ), f"Flag {flag} set to {flag_state} should result in {expected} for '{text}' in '{lang}'"
